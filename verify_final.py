"""验证外网访问"""
import paramiko, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 外网测试
print("=== External access test ===")
urls = [
    ('/', 'Home'),
    ('/knowledge/', 'Knowledge'),
    ('/knowledge/explore/', 'Explore'),
    ('/subscriptions/plans/', 'Plans'),
    ('/admin/', 'Admin'),
]
for url, name in urls:
    code = run(f"curl -s -o /dev/null -w '%{{http_code}}' http://43.134.232.149{url} 2>&1").strip()
    print(f"  http://43.134.232.149{url} -> {code}")

# Celery status
print("\n=== Celery status ===")
result = run("sudo systemctl status celery-worker --no-pager 2>&1")
for line in result.split('\n')[:5]:
    print(line)

result = run("sudo systemctl status celery-beat --no-pager 2>&1")
for line in result.split('\n')[:5]:
    print(line)

# Redis status
print("\n=== Redis ===")
print(run("redis-cli ping 2>&1").strip())

ssh.close()
