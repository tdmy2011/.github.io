"""
部署仪哥安全智库 SaaS 平台到腾讯云服务器 - 修复版
"""
import paramiko
import os
import time
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'
LOCAL_PROJECT = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_django'

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


def main():
    print("=== Deploy SaaS Platform ===\n")
    ssh = connect()
    sftp = ssh.open_sftp()

    total = 0

    # 1. Upload new apps
    for app in NEW_APPS:
        print(f"\n--- {app} ---")
        app_dir = LOCAL_PROJECT + '/' + app
        remote_app = PROJECT_DIR + '/' + app

        # Ensure remote dirs
        for d in [app_dir, app_dir + '/migrations']:
            remote_d = d.replace(LOCAL_PROJECT, PROJECT_DIR).replace('\\', '/')
            try:
                sftp.stat(remote_d)
            except:
                run_cmd(ssh, f"mkdir -p {remote_d}")

        # Upload all files
        for f in os.listdir(app_dir):
            if f.endswith('.py'):
                local = app_dir + '/' + f
                remote = remote_app + '/' + f
                try:
                    sftp.put(local, remote)
                    total += 1
                    print(f"  {app}/{f}")
                except Exception as e:
                    print(f"  ERROR {app}/{f}: {e}")

    # Upload migrations/__init__.py
    for app in NEW_APPS:
        mig_init = LOCAL_PROJECT + '/' + app + '/migrations/__init__.py'
        remote_mig = PROJECT_DIR + '/' + app + '/migrations/__init__.py'
        if os.path.exists(mig_init):
            try:
                sftp.put(mig_init, remote_mig)
                total += 1
                print(f"  {app}/migrations/__init__.py")
            except:
                pass

    # 2. Upload templates
    print("\n--- templates ---")
    for app in NEW_APPS:
        tpl_dir = LOCAL_PROJECT + '/templates/' + app
        if os.path.isdir(tpl_dir):
            remote_tpl = PROJECT_DIR + '/templates/' + app
            run_cmd(ssh, f"mkdir -p {remote_tpl}")
            for f in os.listdir(tpl_dir):
                if f.endswith('.html'):
                    local = tpl_dir + '/' + f
                    remote = remote_tpl + '/' + f
                    try:
                        sftp.put(local, remote)
                        total += 1
                        print(f"  templates/{app}/{f}")
                    except Exception as e:
                        print(f"  ERROR templates/{app}/{f}: {e}")

    # 3. Upload updated files
    print("\n--- updated files ---")
    for f in UPDATED_FILES:
        local = LOCAL_PROJECT + '/' + f
        if os.path.exists(local):
            remote = PROJECT_DIR + '/' + f
            remote_dir = '/'.join(remote.split('/')[:-1])
            run_cmd(ssh, f"mkdir -p {remote_dir}")
            try:
                sftp.put(local, remote)
                total += 1
                print(f"  {f}")
            except Exception as e:
                print(f"  ERROR {f}: {e}")

    print(f"\nTotal uploaded: {total}")
    sftp.close()

    # 4. Migrations
    print("\n=== Migrations ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && "
        f"python manage.py makemigrations knowledge subscriptions ai_engine email_campaigns geo_analytics 2>&1"
    )
    print(result[:800])

    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && "
        f"python manage.py migrate 2>&1"
    )
    print(result[:800])

    # 5. Collect static
    print("\n=== Collect static ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && "
        f"python manage.py collectstatic --noinput 2>&1"
    )
    lines = result.strip().split('\n')
    for line in lines[-3:]:
        print(line)

    # 6. Restart
    print("\n=== Restart ===")
    run_cmd(ssh, "sudo systemctl restart yigeworks 2>&1")
    run_cmd(ssh, "sudo systemctl restart celery-worker celery-beat 2>&1")
    time.sleep(3)

    # 7. Test
    print("\n=== Test ===")
    test_urls = [
        ('/', 'Home'),
        ('/knowledge/', 'Knowledge'),
        ('/knowledge/explore/', 'Explore'),
        ('/subscriptions/plans/', 'Plans'),
        ('/ai/', 'AI Engine'),
        ('/geo/', 'GEO'),
        ('/admin/', 'Admin'),
    ]
    for url, name in test_urls:
        result = run_cmd(ssh,
            f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8000{url} 2>&1"
        )
        code = result.strip()
        ok = code in ('200', '302')
        print(f"  {name}: {code} {'OK' if ok else 'FAIL'}")

    # 8. Django check
    print("\n=== Check ===")
    result = run_cmd(ssh,
        f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1"
    )
    for line in result.split('\n')[:15]:
        print(line)

    print("\n=== Done ===")
    ssh.close()


if __name__ == '__main__':
    main()
