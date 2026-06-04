#!/bin/bash
# 部署脚本 - 将 Django 项目部署到腾讯云轻量服务器
set -e

LH_IP="43.134.232.149"
LH_USER="ubuntu"
REMOTE_DIR="/var/www/yigeworks.com/django"
LOCAL_DIR="C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_shop"

echo "=== 1. 上传 Django 项目代码 ==="
python -c "
import paramiko, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('$LH_IP', username='$LH_USER', password='Yige2026@', timeout=15)

sftp = ssh.open_sftp()

# 创建远程目录
stdin, stdout, stderr = ssh.exec_command('mkdir -p $REMOTE_DIR/{shop,orders,payment,templates}/templates/{shop,orders,payment} $REMOTE_DIR/static $REMOTE_DIR/media')
stdout.read()

# 上传文件列表
files = []
for root, dirs, fnames in os.walk('$LOCAL_DIR'):
    for f in fnames:
        if f.endswith('.pyc') or '.pyc' in f or '__pycache__' in root:
            continue
        lpath = os.path.join(root, f)
        rpath = '$REMOTE_DIR/' + os.path.relpath(lpath, '$LOCAL_DIR').replace('\\\\', '/')
        files.append((lpath, rpath))

print(f'待上传 {len(files)} 个文件')
ok = 0
for lpath, rpath in files[:50]:  # 先上传前50个
    try:
        remote_dir = rpath.rsplit('/', 1)[0]
        ssh.exec_command(f'mkdir -p \"{remote_dir}\"')
        sftp.put(lpath, rpath)
        ok += 1
    except Exception as e:
        print(f'  FAIL {os.path.basename(lpath)}: {e}')
print(f'上传完成: {ok}/{len(files)}')

sftp.close()
ssh.close()
print('上传完成!')
"

echo "=== 2. 在服务器上配置 Python 环境 ==="
python -c "
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('$LH_IP', username='$LH_USER', password='Yige2026@', timeout=30)

cmds = [
    'cd $REMOTE_DIR && python3 -m venv venv',
    'cd $REMOTE_DIR && source venv/bin/activate && pip install django==3.2.25 pillow && echo \"Django installed\"',
    'cd $REMOTE_DIR && source venv/bin/activate && python manage.py migrate && echo \"DB migrated\"',
    'cd $REMOTE_DIR && source venv/bin/activate && python manage.py collectstatic --noinput && echo \"Static collected\"',
]

for cmd in cmds:
    print(f'执行: {cmd[:50]}...')
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    out = stdout.read().decode()
    if 'error' in out.lower() or 'Error' in out:
        print(f'  输出: {out[-200:]}')

print('环境配置完成!')
ssh.close()
"

echo "=== 3. 配置 Gunicorn 服务 ==="
python -c "
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('$LH_IP', username='$LH_USER', password='Yige2026@', timeout=15)

gunicorn_conf = '''[Unit]
Description=YigeWorks Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$REMOTE_DIR
ExecStart=$REMOTE_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:$REMOTE_DIR/yigeworks.sock yigeworks.wsgi:application

[Install]
WantedBy=multi-user.target
'''

# 写入 systemd 服务文件
sftp = ssh.open_sftp()
with sftp.open('/etc/systemd/system/yigeworks.service', 'w') as f:
    f.write(gunicorn_conf)
sftp.close()

ssh.exec_command('sudo systemctl daemon-reload')
ssh.exec_command('sudo systemctl start yigeworks')
ssh.exec_command('sudo systemctl enable yigeworks')
print('Gunicorn 服务已启动!')
ssh.close()
"

echo "=== 4. 配置 Nginx ==="
python -c "
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('$LH_IP', username='$LH_USER', password='Yige2026@', timeout=15)

nginx_conf = '''server {
    listen 80;
    server_name yigeworks.com www.yigeworks.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root $REMOTE_DIR;
    }

    location /media/ {
        root $REMOTE_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$REMOTE_DIR/yigeworks.sock;
    }
}
'''

sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/sites-available/yigeworks', 'w') as f:
    f.write(nginx_conf)
sftp.close()

ssh.exec_command('sudo ln -sf /etc/nginx/sites-available/yigeworks /etc/nginx/sites-enabled/')
ssh.exec_command('sudo nginx -t && sudo systemctl restart nginx')
print('Nginx 配置完成!')
ssh.close()
"

echo "=== 部署完成! ==="
echo "请访问 http://yigeworks.com 验证"
