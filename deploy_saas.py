"""
部署仪哥安全智库 SaaS 平台到腾讯云服务器
通过 paramiko SFTP 上传文件 + SSH 执行远程命令
"""
import paramiko
import os
import time
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

# 服务器配置
HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'

# 本地项目路径
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

# 需要上传的文件列表
NEW_APPS = ['knowledge', 'subscriptions', 'ai_engine', 'email_campaigns', 'geo_analytics']
UPDATED_FILES = [
    'yigeworks/settings.py',
    'yigeworks/urls.py',
    'yigeworks/__init__.py',
    'yigeworks/celery.py',
    'yigeworks/tasks.py',
    'requirements.txt',
    'templates/base.html',
]


def connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
    return ssh


def run_cmd(ssh, cmd, timeout=120):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err


def upload_dir(sftp, local_dir, remote_dir):
    """上传整个目录"""
    uploaded = 0
    for root, dirs, files in os.walk(local_dir):
        for f in files:
            local_path = os.path.join(root, f).replace('\\', '/')
            rel_path = local_path.replace(LOCAL_DIR.replace('\\', '/') + '/', '')
            remote_path = (PROJECT_DIR + '/' + rel_path).replace('\\', '/')

            # 创建远程目录
            remote_dir_path = '/'.join(remote_path.split('/')[:-1])
            try:
                sftp.mkdir(remote_dir_path)
            except:
                pass

            try:
                sftp.put(local_path, remote_path)
                uploaded += 1
                print(f"  uploaded: {rel_path}")
            except Exception as e:
                print(f"  ERROR uploading {rel_path}: {e}")
    return uploaded


def main():
    print("=== 仪哥安全智库 SaaS 平台部署 ===\n")
    ssh = connect()
    sftp = ssh.open_sftp()
    print(f"Connected to {HOST}\n")

    # 1. 上传新应用文件
    total_uploaded = 0
    for app in NEW_APPS:
        local_app_dir = os.path.join(LOCAL_DIR, app)
        print(f"\n--- Uploading {app} ---")
        try:
            # 创建远程目录
            remote_app_dir = PROJECT_DIR + '/' + app
            try:
                sftp.mkdir(remote_app_dir)
            except:
                pass

            # 上传 migrations
            mig_dir = os.path.join(local_app_dir, 'migrations')
            if os.path.exists(mig_dir):
                remote_mig = remote_app_dir + '/migrations'
                try:
                    sftp.mkdir(remote_mig)
                except:
                    pass
                sftp.put(os.path.join(mig_dir, '__init__.py'),
                        remote_mig + '/__init__.py')
                total_uploaded += 1
                print(f"  uploaded: {app}/migrations/__init__.py")

            # 上传所有 .py 和 .html 文件
            for f in os.listdir(local_app_dir):
                if f.endswith('.py') or f.endswith('.html'):
                    local_path = os.path.join(local_app_dir, f)
                    if os.path.isfile(local_path):
                        remote_path = remote_app_dir + '/' + f
                        sftp.put(local_path, remote_path)
                        total_uploaded += 1
                        print(f"  uploaded: {app}/{f}")

        except Exception as e:
            print(f"  ERROR: {e}")

    # 上传模板目录
    for app in NEW_APPS:
        local_tpl_dir = os.path.join(LOCAL_DIR, 'templates', app)
        if os.path.exists(local_tpl_dir):
            print(f"\n--- Uploading templates/{app} ---")
            remote_tpl_dir = PROJECT_DIR + '/templates/' + app
            try:
                sftp.mkdir(remote_tpl_dir)
            except:
                pass
            for f in os.listdir(local_tpl_dir):
                if f.endswith('.html'):
                    local_path = os.path.join(local_tpl_dir, f)
                    remote_path = remote_tpl_dir + '/' + f
                    sftp.put(local_path, remote_path)
                    total_uploaded += 1
                    print(f"  uploaded: templates/{app}/{f}")

    # 2. 上传更新的文件
    print(f"\n--- Uploading updated files ---")
    for f in UPDATED_FILES:
        local_path = os.path.join(LOCAL_DIR, f)
        if os.path.exists(local_path):
            remote_path = PROJECT_DIR + '/' + f.replace('\\', '/')
            remote_dir_path = '/'.join(remote_path.split('/')[:-1])
            try:
                sftp.mkdir(remote_dir_path)
            except:
                pass
            sftp.put(local_path, remote_path)
            total_uploaded += 1
            print(f"  uploaded: {f}")

    print(f"\nTotal uploaded: {total_uploaded} files\n")
    sftp.close()

    # 3. 安装新依赖
    print("=== Installing dependencies ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && "
        f"pip install celery redis django-celery-beat django-celery-results bleach markdown python-dateutil 2>&1"
    )
    print(result[:500])
    if "Successfully installed" in result or "Requirement already satisfied" in result:
        print("Dependencies OK")
    else:
        print("WARNING: Some dependencies may have failed")

    # 4. 数据库迁移
    print("\n=== Database migrations ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py makemigrations "
        f"knowledge subscriptions ai_engine email_campaigns geo_analytics 2>&1"
    )
    print(result[:500])

    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py migrate 2>&1"
    )
    print(result[:500])

    # 5. Collect static
    print("\n=== Collect static ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py collectstatic --noinput 2>&1"
    )
    lines = result.split('\n')
    for line in lines[-5:]:
        print(line)

    # 6. 安装 Redis
    print("\n=== Installing Redis ===")
    result = run_cmd(ssh, "sudo apt-get install -y redis-server 2>&1 | tail -5")
    print(result)
    result = run_cmd(ssh, "sudo systemctl start redis-server && sudo systemctl enable redis-server 2>&1")
    print("Redis started:", result.strip())
    result = run_cmd(ssh, "redis-cli ping 2>&1")
    print("Redis ping:", result.strip())

    # 7. 重启 Gunicorn
    print("\n=== Restart Gunicorn ===")
    result = run_cmd(ssh, "sudo systemctl restart yigeworks 2>&1")
    time.sleep(3)
    result = run_cmd(ssh, "sudo systemctl status yigeworks --no-pager 2>&1")
    status_lines = result.split('\n')
    for line in status_lines[:5]:
        print(line)

    # 8. 启动 Celery Worker 和 Beat
    print("\n=== Starting Celery ===")
    # 先停掉旧的
    run_cmd(ssh, "pkill -f 'celery.*worker' 2>/dev/null; pkill -f 'celery.*beat' 2>/dev/null")
    time.sleep(2)

    # 创建 systemd service 文件
    celery_worker_service = """[Unit]
Description=Celery Worker for YigeWorks
After=network.target redis.service

[Service]
Type=forking
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=yigeworks.settings"
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/celery -A yigeworks worker -l info --logfile=/var/log/celery/worker.log --pidfile=/var/run/celery/worker.pid
ExecStop=/bin/kill -s TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target"""

    celery_beat_service = """[Unit]
Description=Celery Beat for YigeWorks
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=yigeworks.settings"
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/celery -A yigeworks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=/var/log/celery/beat.log --pidfile=/var/run/celery/beat.pid

[Install]
WantedBy=multi-user.target"""

    run_cmd(ssh, "sudo mkdir -p /var/log/celery /var/run/celery && sudo chown ubuntu:ubuntu /var/log/celery /var/run/celery")

    # 通过SFTP写入service文件
    sftp = ssh.open_sftp()
    try:
        with sftp.file('/tmp/celery-worker.service', 'w') as f:
            f.write(celery_worker_service)
        with sftp.file('/tmp/celery-beat.service', 'w') as f:
            f.write(celery_beat_service)
        run_cmd(ssh, "sudo mv /tmp/celery-worker.service /etc/systemd/system/")
        run_cmd(ssh, "sudo mv /tmp/celery-beat.service /etc/systemd/system/")
        run_cmd(ssh, "sudo systemctl daemon-reload")
        run_cmd(ssh, "sudo systemctl enable celery-worker celery-beat")
        run_cmd(ssh, "sudo systemctl start celery-worker celery-beat")
        print("Celery worker and beat started via systemd")
    except Exception as e:
        print(f"Celery systemd setup issue: {e}")
        print("Falling back to nohup...")
        run_cmd(ssh, f"cd {PROJECT_DIR} && source venv/bin/activate && "
                  f"nohup celery -A yigeworks worker -l info > /tmp/celery_worker.log 2>&1 &")
        run_cmd(ssh, f"cd {PROJECT_DIR} && source venv/bin/activate && "
                  f"nohup celery -A yigeworks beat -l info > /tmp/celery_beat.log 2>&1 &")
        time.sleep(3)
        print("Celery started via nohup (fallback)")

    sftp.close()

    # 9. Django check
    print("\n=== Django check ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1"
    )
    print(result)

    # 10. 测试关键页面
    print("\n=== Testing pages ===")
    test_urls = [
        ('/', 'Home'),
        ('/knowledge/', 'Knowledge'),
        ('/subscriptions/plans/', 'Plans'),
        ('/admin/', 'Admin'),
    ]
    for url_path, name in test_urls:
        result = run_cmd(ssh,
            f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8000{url_path} 2>&1"
        )
        status = 'OK' if result.strip() == '200' else f'FAIL ({result.strip()})'
        print(f"  {name}: {status}")

    print("\n=== Deployment complete! ===")
    ssh.close()


if __name__ == '__main__':
    main()
