"""
yigeworks.com Django 部署脚本
通过 paramiko SSH/SFTP 部署到腾讯云轻量服务器
"""
import paramiko
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============ 服务器配置 ============
HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'
VENV_DIR = f'{PROJECT_DIR}/venv'
STATIC_DIR = f'{PROJECT_DIR}/staticfiles'
MEDIA_DIR = f'{PROJECT_DIR}/media'
NGINX_CONF = '/etc/nginx/sites-available/yigeworks.com'


def ssh_exec(ssh, cmd):
    """执行远程命令并返回输出"""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    exit_code = stdout.channel.recv_exit_status()
    return out, err, exit_code


def deploy():
    local_project = os.path.dirname(os.path.abspath(__file__))

    # 连接服务器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'正在连接 {HOST}...')
    ssh.connect(HOST, username=USER, password=PASSWORD, allow_agent=False, look_for_keys=False)
    print('已连接')

    # 1. 上传项目文件
    print('\n[1/7] 上传项目文件...')
    sftp = ssh.open_sftp()

    # 确保远程目录存在
    for d in [PROJECT_DIR, STATIC_DIR, MEDIA_DIR]:
        try:
            sftp.stat(d)
        except FileNotFoundError:
            ssh_exec(ssh, f'sudo mkdir -p {d} && sudo chown {USER}:{USER} {d}')

    # 上传所有文件
    upload_count = 0
    skip_dirs = {'venv', 'staticfiles', '__pycache__', '.git', 'media',
                'node_modules', '*.pyc'}
    for root, dirs, files in os.walk(local_project):
        # 跳过不需要上传的目录
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.endswith('.pyc')]
        rel_root = os.path.relpath(root, local_project).replace('\\', '/')
        remote_root = (PROJECT_DIR + '/' + rel_root).rstrip('/') if rel_root != '.' else PROJECT_DIR
        # 确保远程目录存在
        try:
            sftp.stat(remote_root)
        except FileNotFoundError:
            try:
                sftp.mkdir(remote_root)
            except Exception:
                ssh_exec(ssh, f'mkdir -p {remote_root}')
        for f in files:
            if f.endswith(('.pyc', '.pyo', '.db', '.DS_Store')):
                continue
            local_path = os.path.join(root, f)
            remote_path = (remote_root + '/' + f).replace('\\', '/')
            try:
                sftp.put(local_path, remote_path)
                upload_count += 1
            except Exception as e:
                print(f'  跳过: {rel_root}/{f} ({e})')

    sftp.close()
    print(f'  上传 {upload_count} 个文件')

    # 2. 创建虚拟环境
    print('\n[2/7] 配置虚拟环境...')
    out, err, code = ssh_exec(ssh, f'test -d {VENV_DIR}/bin && echo "exists" || echo "new"')
    if 'new' in out:
        ssh_exec(ssh, f'python3 -m venv {VENV_DIR}')
        print('  虚拟环境已创建')
    else:
        print('  虚拟环境已存在')

    # 3. 安装依赖
    print('\n[3/7] 安装 Python 依赖...')
    out, err, code = ssh_exec(ssh, f'{VENV_DIR}/bin/pip install -r {PROJECT_DIR}/requirements.txt')
    if code != 0:
        print(f'  pip 安装可能有问题: {err[:200]}')
    else:
        print('  依赖安装完成')

    # 4. 数据库迁移
    print('\n[4/7] 运行数据库迁移...')
    out, err, code = ssh_exec(ssh, f'cd {PROJECT_DIR} && {VENV_DIR}/bin/python manage.py makemigrations')
    out, err, code = ssh_exec(ssh, f'cd {PROJECT_DIR} && {VENV_DIR}/bin/python manage.py migrate')
    if code != 0:
        print(f'  迁移警告: {err[:300]}')
    else:
        print('  数据库迁移完成')

    # 5. 收集静态文件
    print('\n[5/7] 收集静态文件...')
    out, err, code = ssh_exec(ssh, f'cd {PROJECT_DIR} && {VENV_DIR}/bin/python manage.py collectstatic --noinput')
    if code != 0:
        print(f'  collectstatic 警告: {err[:300]}')
    else:
        print('  静态文件收集完成')

    # 6. 创建超级用户（如果不存在）
    print('\n[6/7] 检查超级用户...')
    out, err, code = ssh_exec(ssh,
        f'cd {PROJECT_DIR} && {VENV_DIR}/bin/python manage.py shell -c "'
        'from django.contrib.auth import get_user_model; User=get_user_model(); '
        'if not User.objects.filter(is_superuser=True).exists(): '
        'User.objects.create_superuser(\"admin\", \"yjurado860@gmail.com\", \"Yige2026@\"); '
        'print(\"admin user created\")'
        'else: print(\"admin user exists\")"')
    print(f'  {out.strip()}')

    # 7. 配置 Gunicorn + Nginx
    print('\n[7/7] 配置 Gunicorn + Nginx...')

    # Gunicorn systemd service
    gunicorn_service = f'''[Unit]
Description=YigeWorks Django Gunicorn
After=network.target

[Service]
User={USER}
Group={USER}
WorkingDirectory={PROJECT_DIR}
ExecStart={VENV_DIR}/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 --timeout 120 yigeworks.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''
    sftp = ssh.open_sftp()
    with sftp.open(f'/tmp/yigeworks.service', 'w') as f:
        f.write(gunicorn_service)
    sftp.close()
    ssh_exec(ssh, 'sudo cp /tmp/yigeworks.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable yigeworks && sudo systemctl restart yigeworks')

    # Nginx config
    nginx_conf = f'''server {{
    listen 80;
    server_name yigeworks.com www.yigeworks.com;

    client_max_body_size 50M;

    location /static/ {{
        alias {STATIC_DIR}/;
        expires 30d;
    }}

    location /media/ {{
        alias {MEDIA_DIR}/;
        expires 7d;
    }}

    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
'''
    sftp = ssh.open_sftp()
    with sftp.open(f'/tmp/yigeworks_nginx', 'w') as f:
        f.write(nginx_conf)
    sftp.close()
    ssh_exec(ssh, f'sudo cp /tmp/yigeworks_nginx {NGINX_CONF} && '
                  f'sudo ln -sf {NGINX_CONF} /etc/nginx/sites-enabled/yigeworks.com && '
                  f'sudo nginx -t && sudo systemctl reload nginx')

    print('  Nginx 配置完成')

    # 验证
    print('\n验证部署...')
    out, err, code = ssh_exec(ssh, 'curl -s -o /dev/null -w "%{http_code}" http://localhost:80')
    print(f'  HTTP 状态码: {out.strip()}')

    out, err, code = ssh_exec(ssh, 'sudo systemctl is-active yigeworks')
    print(f'  Gunicorn 状态: {out.strip()}')

    out, err, code = ssh_exec(ssh, 'sudo systemctl is-active nginx')
    print(f'  Nginx 状态: {out.strip()}')

    ssh.close()
    print('\n部署完成！')
    print(f'管理后台: http://{HOST}/admin/')
    print(f'管理员账号: admin / Yige2026@')
    print(f'\n重要：DNS 需要将 yigeworks.com A 记录指向 {HOST}')


if __name__ == '__main__':
    deploy()
