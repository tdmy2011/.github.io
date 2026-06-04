"""
诊断部署失败原因
"""
import paramiko

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER, username=USER, password=PASS, timeout=15)

def run(cmd, timeout=30):
    print(f"\nCMD: {cmd[:150]}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out.strip():
        print(f"OUT:\n{out[:1000]}")
    if err.strip():
        print(f"ERR:\n{err[:1000]}")
    return out, err

# 1. Check Gunicorn status
print("="*60)
print("1. Gunicorn status")
print("="*60)
run('sudo systemctl status yigeworks --no-pager -l')

# 2. Check Gunicorn error log
print("\n" + "="*60)
print("2. Gunicorn logs (last 30 lines)")
print("="*60)
run('sudo journalctl -u yigeworks --no-pager -n 30')

# 3. Check if venv exists
print("\n" + "="*60)
print("3. Check venv and project files")
print("="*60)
run(f'ls -la {PROJECT_DIR}/venv/bin/')
run(f'ls -la {PROJECT_DIR}/book_commodity/')
run(f'ls -la {PROJECT_DIR}/book_shopper/')
run(f'ls -la {PROJECT_DIR}/book_index/')

# 4. Try Django check
print("\n" + "="*60)
print("4. Django check")
print("="*60)
run(f'cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1')

# 5. Try importing the apps
print("\n" + "="*60)
print("5. Import test")
print("="*60)
for app in ['book_index', 'book_commodity', 'book_shopper']:
    run(f"cd {PROJECT_DIR} && source venv/bin/activate && python -c \"import sys; sys.path.insert(0, '.'); from {app}.apps import *; print('{app}: OK')\" 2>&1")

# 6. Read apps.py to check name
print("\n" + "="*60)
print("6. apps.py contents")
print("="*60)
for app in ['book_index', 'book_commodity', 'book_shopper']:
    run(f'cat {PROJECT_DIR}/{app}/apps.py')

# 7. Try to start Gunicorn manually to see error
print("\n" + "="*60)
print("7. Manual Gunicorn start test")
print("="*60)
run(f'cd {PROJECT_DIR} && source venv/bin/activate && timeout 5 gunicorn yigeworks.wsgi:application --bind 127.0.0.1:9000 2>&1 || true')

ssh.close()
print("\nDone")
