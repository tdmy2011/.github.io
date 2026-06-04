"""
读取 chapter11 的核心代码文件
"""
import paramiko

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
SRC = '/home/ubuntu/django3web_src/extracted/chapter11/babys'

def cat(ssh, path):
    stdin, stdout, stderr = ssh.exec_command(f'cat {path}', timeout=15)
    return stdout.read().decode('utf-8', errors='replace')

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)

    files = [
        f'{SRC}/index/models.py',
        f'{SRC}/index/views.py',
        f'{SRC}/index/urls.py',
        f'{SRC}/index/admin.py',
        f'{SRC}/commodity/models.py',
        f'{SRC}/commodity/views.py',
        f'{SRC}/commodity/urls.py',
        f'{SRC}/commodity/admin.py',
        f'{SRC}/shopper/models.py',
        f'{SRC}/shopper/views.py',
        f'{SRC}/shopper/urls.py',
        f'{SRC}/shopper/admin.py',
        f'{SRC}/babys/urls.py',
        f'{SRC}/babys/settings.py',
        f'{SRC}/templates/base.html',
        f'{SRC}/templates/index.html',
        f'{SRC}/templates/commodity.html',
        f'{SRC}/templates/details.html',
        f'{SRC}/templates/shopcart.html',
        f'{SRC}/templates/shopper.html',
        f'{SRC}/templates/login.html',
    ]

    for f in files:
        print(f"\n{'='*60}")
        print(f"FILE: {f}")
        print('='*60)
        content = cat(ssh, f)
        print(content)

    # Also check chapter6 special projects
    print(f"\n{'='*60}")
    print(f"chapter6/6.4/MyDjango/index/models.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.4/MyDjango/index/models.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.4/MyDjango/index/views.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.4/MyDjango/index/views.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.5/MyDjango/index/models.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.5/MyDjango/index/models.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.5/MyDjango/index/views.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.5/MyDjango/index/views.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.6/MyDjango/mydefined/templatetags/myfilter.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.6/MyDjango/mydefined/templatetags/myfilter.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.6/MyDjango/index/views.py")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.6/MyDjango/index/views.py'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.6/MyDjango/templates/index.html")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.6/MyDjango/templates/index.html'))
    print(f"\n{'='*60}")
    print(f"chapter6/6.6/MyDjango/templates/base.html")
    print('='*60)
    print(cat(ssh, f'/home/ubuntu/django3web_src/extracted/chapter6/6.6/MyDjango/templates/base.html'))

    ssh.close()

if __name__ == '__main__':
    main()
