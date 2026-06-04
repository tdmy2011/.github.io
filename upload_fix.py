"""
上传修复后的 __init__.py 并重启服务
"""
import paramiko
import os
import time

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
sftp = ssh.open_sftp()
print("Connected")

PROJECT_LOCAL = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

# Upload the 3 __init__.py files
files = [
    ('book_index/__init__.py', PROJECT_DIR + '/book_index/__init__.py'),
    ('book_commodity/__init__.py', PROJECT_DIR + '/book_commodity/__init__.py'),
    ('book_shopper/__init__.py', PROJECT_DIR + '/book_shopper/__init__.py'),
]
for local_rel, remote_path in files:
    local = os.path.join(PROJECT_LOCAL, local_rel)
    sftp.put(local, remote_path)
    print(f"  UP: {os.path.basename(os.path.dirname(local_rel))}/__init__.py")

sftp.close()

# Now test Django check
print("\n=== Django check ===")
stdin, stdout, stderr = ssh.exec_command(
    f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1',
    timeout=30
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f"OUT:\n{out}")
if err.strip():
    print(f"ERR:\n{err}")

# Make migrations
print("\n=== makemigrations book_* ===")
stdin, stdout, stderr = ssh.exec_command(
    f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py makemigrations book_commodity book_shopper 2>&1',
    timeout=60
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f"OUT:\n{out}")
if err.strip():
    print(f"ERR:\n{err[:500]}")

# Migrate
print("\n=== migrate ===")
stdin, stdout, stderr = ssh.exec_command(
    f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py migrate 2>&1',
    timeout=60
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f"OUT:\n{out[:1000]}")
if err.strip():
    print(f"ERR:\n{err[:300]}")

# Collect static
print("\n=== collectstatic ===")
stdin, stdout, stderr = ssh.exec_command(
    f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py collectstatic --noinput 2>&1',
    timeout=120
)
out = stdout.read().decode('utf-8', errors='replace')
print(f"OUT:\n{out[:500]}")

# Restart Gunicorn
print("\n=== Restarting Gunicorn ===")
stdin, stdout, stderr = ssh.exec_command('sudo systemctl restart yigeworks', timeout=15)
time.sleep(4)

# Verify
print("\n=== Verification ===")
pages = [
    ('/', 'Main site'),
    ('/admin/', 'Admin'),
    ('/book/', 'Book index'),
    ('/book/commodity/', 'Book commodity'),
    ('/blog/', 'Blog'),
    ('/products/', 'Products'),
    ('/shop/cart/', 'Cart'),
]
for url, name in pages:
    stdin, stdout, stderr = ssh.exec_command(
        f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:8000{url}",
        timeout=10
    )
    code = stdout.read().decode().strip()
    status = "OK" if code == '200' else f"WARN({code})"
    print(f"  {name:25} {url:30} -> {status}")

# External
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' http://43.134.232.149/book/ 2>&1",
    timeout=10
)
code = stdout.read().decode().strip()
print(f"\n  External /book/: {code}")

ssh.close()
print("\nDone!")
