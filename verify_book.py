import paramiko, os, time

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'
PROJECT_LOCAL = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
sftp = ssh.open_sftp()
print("Connected")

# Upload 3 urls.py
files = [
    (os.path.join(PROJECT_LOCAL, 'book_index', 'urls.py'), PROJECT_DIR + '/book_index/urls.py'),
    (os.path.join(PROJECT_LOCAL, 'book_commodity', 'urls.py'), PROJECT_DIR + '/book_commodity/urls.py'),
    (os.path.join(PROJECT_LOCAL, 'book_shopper', 'urls.py'), PROJECT_DIR + '/book_shopper/urls.py'),
]
for local, remote in files:
    sftp.put(local, remote)
    print("  UP: " + os.path.basename(os.path.dirname(local)) + "/urls.py")

sftp.close()

# Django check
print("\n=== Django check ===")
stdin, stdout, stderr = ssh.exec_command(
    'cd ' + PROJECT_DIR + ' && source venv/bin/activate && python manage.py check 2>&1', timeout=30)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out[:1000])
if err.strip():
    print("ERR:\n" + err[:500])

# Restart Gunicorn
print("\n=== Restarting Gunicorn ===")
ssh.exec_command('sudo systemctl restart yigeworks')
time.sleep(4)

# Verify
print("\n=== Verification ===")
pages = [
    ('/', 'Main site'),
    ('/admin/', 'Admin'),
    ('/book/', 'Book index'),
    ('/book/commodity/', 'Book commodity'),
    ('/book/shopper/', 'Book shopper'),
    ('/blog/', 'Blog'),
    ('/products/', 'Products'),
    ('/shop/cart/', 'Cart'),
]
for url, name in pages:
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000" + url, timeout=10)
    code = stdout.read().decode().strip()
    status = "OK" if code == '200' else "WARN(" + code + ")"
    print("  " + name + ": " + status)

# External
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' http://43.134.232.149/book/ 2>&1", timeout=10)
code = stdout.read().decode().strip()
print("\n  External /book/: " + code)

ssh.close()
print("\nDone!")
