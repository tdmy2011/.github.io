"""诊断部署问题"""
import paramiko
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

def run(cmd, timeout=60):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 1. Get full error
print("=== Django check full error ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1", 30)
print(result)

# 2. Try importing settings
print("\n=== Import test ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python -c 'from yigeworks import settings; print(\"Settings OK\")' 2>&1", 15)
print(result)

# 3. Check installed packages
print("\n=== Installed celery packages ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && pip list | grep -i celery 2>&1", 15)
print(result)

# 4. Check if Gunicorn can start
print("\n=== Gunicorn status ===")
result = run("sudo systemctl status yigeworks --no-pager -l 2>&1", 15)
lines = result.split('\n')
for line in lines[:15]:
    print(line)

# 5. Try Gunicorn error log
print("\n=== Gunicorn journal ===")
result = run("sudo journalctl -u yigeworks --no-pager -n 30 2>&1", 15)
print(result[-1500:])

ssh.close()
