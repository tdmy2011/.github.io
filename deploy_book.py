"""
部署 Django3-Web 集成到腾讯云服务器
"""
import paramiko
import os
import time

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'
SRC_STATIC = '/home/ubuntu/django3web_src/extracted/chapter11/babys/pstatic'
PROJECT_LOCAL = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

def ssh_run(ssh, cmd, timeout=60):
    print(f"  CMD: {cmd[:120]}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out.strip():
        print(f"  OUT: {out.strip()[:500]}")
    if err.strip():
        print(f"  ERR: {err.strip()[:300]}")
    return out, err

def upload_file(sftp, local_path, remote_path):
    os.makedirs(os.path.dirname(remote_path.replace('\\', '/')), exist_ok=True)
    try:
        sftp.put(local_path, remote_path)
        print(f"  UP: {remote_path}")
    except Exception as e:
        print(f"  FAIL: {remote_path} - {e}")

def upload_dir(sftp, local_dir, remote_dir):
    count = 0
    for root, dirs, files in os.walk(local_dir):
        rel = os.path.relpath(root, local_dir).replace('\\', '/')
        remote = (remote_dir + '/' + rel).rstrip('/') if rel != '.' else remote_dir
        try:
            sftp.mkdir(remote)
        except:
            pass
        for f in files:
            local_path = os.path.join(root, f)
            remote_path = remote + '/' + f
            try:
                sftp.put(local_path, remote_path)
                count += 1
            except Exception as e:
                print(f"  FAIL: {remote_path} - {e}")
    return count

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
    sftp = ssh.open_sftp()
    print("Connected")

    # ============ 1. Upload new app directories ============
    for app in ['book_index', 'book_commodity', 'book_shopper']:
        local_app = os.path.join(PROJECT_LOCAL, app)
        remote_app = PROJECT_DIR + '/' + app
        print(f"\n=== Uploading {app} ===")
        n = upload_dir(sftp, local_app, remote_app)
        print(f"  Uploaded {n} files")

    # ============ 2. Upload book templates ============
    local_tpl = os.path.join(PROJECT_LOCAL, 'templates', 'book')
    remote_tpl = PROJECT_DIR + '/templates/book'
    print(f"\n=== Uploading book templates ===")
    n = upload_dir(sftp, local_tpl, remote_tpl)
    print(f"  Uploaded {n} files")

    # ============ 3. Copy static files from source on server ============
    print("\n=== Copying static files ===")
    BOOK_STATIC = PROJECT_DIR + '/static/book'
    ssh_run(ssh, f'mkdir -p {BOOK_STATIC}')
    ssh_run(ssh, f'cp -r {SRC_STATIC}/* {BOOK_STATIC}/ 2>&1')
    ssh_run(ssh, f'ls -la {BOOK_STATIC}/')

    # ============ 4. Upload updated config files ============
    print("\n=== Uploading config files ===")
    upload_file(sftp,
        os.path.join(PROJECT_LOCAL, 'yigeworks', 'settings.py'),
        PROJECT_DIR + '/yigeworks/settings.py')
    upload_file(sftp,
        os.path.join(PROJECT_LOCAL, 'yigeworks', 'urls.py'),
        PROJECT_DIR + '/yigeworks/urls.py')
    upload_file(sftp,
        os.path.join(PROJECT_LOCAL, 'requirements.txt'),
        PROJECT_DIR + '/requirements.txt')

    # ============ 5. Install dependencies ============
    print("\n=== Installing dependencies ===")
    ssh_run(ssh, f'cd {PROJECT_DIR} && source venv/bin/activate && pip install alipay-sdk-python 2>&1 | tail -5', timeout=120)

    # ============ 6. Run migrations ============
    print("\n=== Running migrations ===")
    ssh_run(ssh, f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py makemigrations book_commodity book_shopper 2>&1', timeout=60)
    ssh_run(ssh, f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py migrate 2>&1', timeout=60)

    # ============ 7. Collect static ============
    print("\n=== Collecting static ===")
    ssh_run(ssh, f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py collectstatic --noinput 2>&1', timeout=120)

    # ============ 8. Restart ============
    print("\n=== Restarting ===")
    ssh_run(ssh, 'sudo systemctl restart yigeworks')

    # ============ 9. Verify ============
    time.sleep(3)
    print("\n=== Verification ===")
    # First test the main site still works
    pages = [
        ('/', 'Main site'),
        ('/admin/', 'Admin'),
        ('/book/', 'Book index'),
        ('/book/commodity/', 'Book commodity list'),
        ('/blog/', 'Blog'),
        ('/products/', 'Products'),
        ('/shop/cart/', 'Cart'),
    ]
    for url, name in pages:
        out, _ = ssh_run(ssh, f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:8000{url}")
        code = out.strip()
        status = "OK" if code == '200' else f"WARN({code})"
        print(f"  {name:25} {url:30} -> {status}")

    # Test external access
    print("\n=== External access ===")
    out, _ = ssh_run(ssh, "curl -s -o /dev/null -w '%{http_code}' http://43.134.232.149/book/")
    print(f"  External /book/: {out.strip()}")

    sftp.close()
    ssh.close()
    print("\nDone!")

if __name__ == '__main__':
    main()
