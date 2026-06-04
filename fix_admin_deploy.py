"""上传修复并运行migration"""
import paramiko
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
PROJECT_DIR = '/home/ubuntu/yigeworks_django'
LOCAL = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
sftp = ssh.open_sftp()

def run(cmd, timeout=120):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# Upload fixed admin files
for f in ['ai_engine/admin.py', 'geo_analytics/admin.py']:
    sftp.put(LOCAL + '/' + f, PROJECT_DIR + '/' + f)
    print(f"Uploaded {f}")

sftp.close()

# Run migrations
print("\n=== makemigrations ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py makemigrations knowledge subscriptions ai_engine email_campaigns geo_analytics 2>&1")
print(result[:1000])

print("\n=== migrate ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py migrate 2>&1")
print(result[:1000])

# Restart
print("\n=== Restart ===")
run("sudo systemctl restart yigeworks 2>&1")

# Test
import time
time.sleep(3)
print("\n=== Test ===")
urls = [('/', 'Home'), ('/knowledge/', 'Knowledge'), ('/knowledge/explore/', 'Explore'),
        ('/subscriptions/plans/', 'Plans'), ('/admin/', 'Admin')]
for url, name in urls:
    code = run(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8000{url} 2>&1").strip()
    print(f"  {name}: {code} {'OK' if code in ('200','302') else 'FAIL'}")

# Check
print("\n=== Check ===")
result = run(f"cd {PROJECT_DIR} && source venv/bin/activate && python manage.py check 2>&1")
print(result[:500])

ssh.close()
