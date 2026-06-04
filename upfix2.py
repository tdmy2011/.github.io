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

# Upload 3 __init__.py files
files = [
    ('book_index/__init__.py', PROJECT_DIR + '/book_index/__init__.py'),
    ('book_commodity/__init__.py', PROJECT_DIR + '/book_commodity/__init__.py'),
    ('book_shopper/__init__.py', PROJECT_DIR + '/book_shopper/__init__.py'),
]
for local_rel, remote_path in files:
    local_path = os.path.join(PROJECT_LOCAL, local_rel)
    sftp.put(local_path, remote_path)
    print("  UP: " + os.path.basename(os.path.dirname(local_rel)) + "/__init__.py")

sftp.close()

# Test Django check
print("\n=== Django check ===")
stdin, stdout, stderr = ssh.exec_command(
    'cd ' + PROJECT_DIR + ' && source venv/bin/activate && python manage.py check 2>&1',
    timeout=30
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("OUT:\n" + out[:1000])
if err.strip():
    print("ERR:\n" + err[:500])

# makemigrations
print("\n=== makemigrations ===")
stdin, stdout, stderr = ssh.exec_command(
    'cd ' + PROJECT_DIR + ' && source venv/bin/activate && python manage.py makemigrations book_commodity book_shopper 2>&1',
    timeout=60
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("OUT:\n" + out[:1000])
if err.strip():
    print("ERR:\n" + err[:500])

# migrate
print("\n=== migrate ===")
stdin, stdout, stderr = ssh.exec_command(
    'cd ' + PROJECT_DIR + ' && source venv/bin/activate && python manage.py migrate 2>&1',
    timeout=60
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("OUT:\n" + out[:1000])
if err.strip():
    print("ERR:\n" + err[:500])

# collectstatic
print("\n=== collectstatic ===")
stdin, stdout, stderr = ssh.exec_command(
    'cd ' + PROJECT_DIR + ' && source venv/bin/activate && python manage.py collectstatic --noinput 2>&1',
    timeout=120
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("OUT:\n" + out[:500])
if err.strip():
    print("ERR:\n" + err[:300])

# Restart
print("\n=== Restarting Gunicorn ===")
ssh.exec_command('sudo systemctl restart yigeworks')
time.sleep(4)

# Verify
print("\n=== Verification ===")
pages = ['/', '/admin/', '/book/', '/book/commodity/', '/blog/', '/products/', '/shop/cart/']
for url in pages:
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000" + url,
        timeout=10
    )
    code = stdout.read().decode().strip()
    status = "OK" if code == '200' else "WARN(" + code + ")"
    print("  " + url + " -> " + status)

stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' http://43.134.232.149/book/ 2>&1",
    timeout=10
)
code = stdout.read().decode().strip()
print("\n  External /book/: " + code)

ssh.close()
print("\nDone!")
