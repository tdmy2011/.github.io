"""修复admin readonly_fields问题"""
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

# 找出哪个admin有问题
print("=== Checking admin files for readonly_fields issues ===")
for app in ['knowledge', 'subscriptions', 'ai_engine', 'email_campaigns', 'geo_analytics']:
    result = run(f"grep -n 'readonly_fields' {PROJECT_DIR}/{app}/admin.py 2>&1")
    if result.strip():
        print(f"\n--- {app}/admin.py ---")
        print(result)

# 也检查 views.py 中的问题
print("\n=== Checking for import issues ===")
for app in ['knowledge', 'subscriptions', 'ai_engine', 'email_campaigns', 'geo_analytics']:
    result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python -c 'from {app}.admin import *; print(\"{app} admin OK\")' 2>&1")
    print(result.strip())

ssh.close()
