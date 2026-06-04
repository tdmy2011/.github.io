"""
deploy_official_site.py
一键部署 official_site 应用到服务器
使用 paramiko SFTP 上传所有文件，然后在服务器执行 migrate
"""
import paramiko
import os

HOST = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
LOCAL_BASE = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'
REMOTE_BASE = '/home/ubuntu/yigeworks_django'
VENV_PYTHON = f'{REMOTE_BASE}/venv/bin/python'

# ===== 文件清单 =====
FILES = [
    # official_site app
    ('official_site/__init__.py', 'official_site/__init__.py'),
    ('official_site/apps.py', 'official_site/apps.py'),
    ('official_site/models.py', 'official_site/models.py'),
    ('official_site/views.py', 'official_site/views.py'),
    ('official_site/urls.py', 'official_site/urls.py'),
    ('official_site/admin.py', 'official_site/admin.py'),
    ('official_site/migrations/__init__.py', 'official_site/migrations/__init__.py'),
    # static
    ('official_site/static/official_site/css/main.css',
     'official_site/static/official_site/css/main.css'),
    # templates
    ('templates/official_site/base.html', 'templates/official_site/base.html'),
    ('templates/official_site/home.html', 'templates/official_site/home.html'),
    ('templates/official_site/about.html', 'templates/official_site/about.html'),
    ('templates/official_site/product.html', 'templates/official_site/product.html'),
    ('templates/official_site/product_detail.html', 'templates/official_site/product_detail.html'),
    ('templates/official_site/news.html', 'templates/official_site/news.html'),
    ('templates/official_site/news_detail.html', 'templates/official_site/news_detail.html'),
    ('templates/official_site/contact.html', 'templates/official_site/contact.html'),
    ('templates/official_site/download.html', 'templates/official_site/download.html'),
    # updated settings & urls
    ('yigeworks/settings.py', 'yigeworks/settings.py'),
    ('yigeworks/urls.py', 'yigeworks/urls.py'),
]

def ensure_remote_dir(sftp, remote_path):
    parts = remote_path.replace('\\', '/').split('/')
    current = ''
    for part in parts:
        if not part:
            continue
        current += '/' + part
        try:
            sftp.stat(current)
        except FileNotFoundError:
            sftp.mkdir(current)

def main():
    print(f'Connecting to {HOST}...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS)
    sftp = ssh.open_sftp()

    print('Uploading files...')
    for local_rel, remote_rel in FILES:
        local_path = os.path.join(LOCAL_BASE, local_rel.replace('/', os.sep))
        remote_path = f'{REMOTE_BASE}/{remote_rel}'
        remote_dir = remote_path.rsplit('/', 1)[0]
        ensure_remote_dir(sftp, remote_dir)
        print(f'  ↑ {local_rel}')
        sftp.put(local_path, remote_path)

    sftp.close()

    print('\nRunning migrations on server...')
    cmds = [
        f'cd {REMOTE_BASE} && {VENV_PYTHON} manage.py makemigrations official_site 2>&1',
        f'cd {REMOTE_BASE} && {VENV_PYTHON} manage.py migrate official_site 2>&1',
        f'cd {REMOTE_BASE} && {VENV_PYTHON} manage.py collectstatic --noinput 2>&1 | tail -5',
        'sudo systemctl restart yigeworks.service',
    ]
    for cmd in cmds:
        print(f'\n$ {cmd}')
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out: print(out)
        if err: print('[STDERR]', err)

    print('\nVerifying HTTP status...')
    _, stdout, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/site/')
    print(f'  /site/ → HTTP {stdout.read().decode()}')

    ssh.close()
    print('\nDone!')

if __name__ == '__main__':
    main()
