#!/usr/bin/env python3
"""
deploy_django.py - 部署 Django 项目到腾讯云轻量服务器
"""
import paramiko
import os
import sys

# 服务器信息
LH_IP = '43.134.232.149'
LH_USER = 'ubuntu'
LH_PASS = 'Yige2026@'
LOCAL_DIR = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_shop'
REMOTE_DIR = '/var/www/yigeworks.com/django'

def deploy():
    print('=== YigeWorks Django 部署脚本 ===\n')

    # 1. 连接服务器
    print('[1/6] 连接服务器...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(LH_IP, username=LH_USER, password=LH_PASS, timeout=15)
        print('  ✅ SSH 连接成功\n')
    except Exception as e:
        print(f'  ❌ SSH 连接失败: {e}')
        sys.exit(1)

    sftp = ssh.open_sftp()

    # 2. 创建远程目录
    print('[2/6] 创建远程目录...')
    cmds = [
        f'mkdir -p {REMOTE_DIR}',
        f'mkdir -p {REMOTE_DIR}/shop/templates/shop',
        f'mkdir -p {REMOTE_DIR}/orders/templates/orders',
        f'mkdir -p {REMOTE_DIR}/payment/templates/payment',
        f'mkdir -p {REMOTE_DIR}/templates',
        f'mkdir -p {REMOTE_DIR}/static',
        f'mkdir -p {REMOTE_DIR}/media',
        f'chown -R ubuntu:ubuntu {REMOTE_DIR}',
    ]
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.read()
    print('  ✅ 远程目录创建完成\n')

    # 3. 上传文件
    print('[3/6] 上传项目文件...')

    # 收集所有需要上传的文件
    upload_files = []

    # Python 文件
    for root, dirs, files in os.walk(LOCAL_DIR):
        # 跳过 __pycache__ 和 .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'staticfiles']]
        for f in files:
            if f.endswith('.pyc') or f.startswith('.'):
                continue
            local_path = os.path.join(root, f)
            rel_path = os.path.relpath(local_path, LOCAL_DIR)
            remote_path = REMOTE_DIR + '/' + rel_path.replace('\\', '/')
            upload_files.append((local_path, remote_path))

    print(f'  待上传 {len(upload_files)} 个文件')
    ok = 0
    for local_path, remote_path in upload_files:
        try:
            remote_dir = remote_path.rsplit('/', 1)[0]
            ssh.exec_command(f'mkdir -p "{remote_dir}"')
            sftp.put(local_path, remote_path)
            ok += 1
        except Exception as e:
            print(f'  ⚠️  {os.path.basename(local_path)}: {e}')

    print(f'  ✅ 上传完成: {ok}/{len(upload_files)} 个文件\n')

    # 4. 配置 Python 环境
    print('[4/6] 配置 Python 环境...')
    cmds = [
        f'cd {REMOTE_DIR} && python3 -m venv venv',
        f'cd {REMOTE_DIR} && source venv/bin/activate && pip install -q django==3.2.25 pillow && echo "Django OK"',
    ]
    for cmd in cmds:
        print(f'  执行: {cmd[50:]}...')
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        import time
        time.sleep(2)
        output = stdout.read().decode()
        if 'OK' in output or 'Success' in output or 'already' in output.lower():
            print('  ✅ 成功')
        else:
            print(f'  输出: {output[-100:]}')

    print()

    # 5. 数据库迁移
    print('[5/6] 数据库迁移...')
    cmd = f'cd {REMOTE_DIR} && source venv/bin/activate && python manage.py migrate --noinput'
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    import time
    time.sleep(3)
    output = stdout.read().decode()
    if 'OK' in output or 'No migrations' in output or 'Applying' in output:
        print('  ✅ 数据库迁移完成')
    else:
        print(f'  输出: {output[-200:]}')
    print()

    # 6. 配置 Gunicorn + Nginx
    print('[6/6] 配置 Gunicorn + Nginx...')

    # 创建 Gunicorn 服务文件
    gunicorn_service = f'''[Unit]
Description=YigeWorks Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory={REMOTE_DIR}
ExecStart={REMOTE_DIR}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:{REMOTE_DIR}/yigeworks.sock yigeworks.wsgi:application

[Install]
WantedBy=multi-user.target
'''

    # 创建 Nginx 配置
    nginx_conf = f'''server {{
    listen 80;
    server_name yigeworks.com www.yigeworks.com;

    location = /favicon.ico {{
        access_log off;
        log_not_found off;
    }}

    location /static/ {{
        root {REMOTE_DIR};
    }}

    location /media/ {{
        root {REMOTE_DIR};
    }}

    location / {{
        include proxy_params;
        proxy_pass http://unix:{REMOTE_DIR}/yigeworks.sock;
    }}
}}
'''

    # 写入服务文件
    with sftp.open(f'/etc/systemd/system/yigeworks.service', 'w') as f:
        f.write(gunicorn_service)
    print('  ✅ Gunicorn 服务文件已创建')

    # 写入 Nginx 配置
    with sftp.open('/etc/nginx/sites-available/yigeworks', 'w') as f:
        f.write(nginx_conf)
    print('  ✅ Nginx 配置已创建')

    # 启用配置
    cmds = [
        'sudo systemctl daemon-reload',
        'sudo systemctl start yigeworks',
        'sudo systemctl enable yigeworks',
        'sudo ln -sf /etc/nginx/sites-available/yigeworks /etc/nginx/sites-enabled/',
        'sudo nginx -t',
        'sudo systemctl restart nginx',
    ]
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if 'error' in error.lower() or 'failed' in error.lower():
            print(f'  ⚠️  {cmd}: {error[-100:]}')
        else:
            print(f'  ✅ {cmd[:50]}...')

    print()
    print('=== 部署完成! ===')
    print(f'请访问: http://yigeworks.com')
    print(f'或 IP: http://{LH_IP}')

    sftp.close()
    ssh.close()

if __name__ == '__main__':
    deploy()
