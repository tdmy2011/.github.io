"""修复Celery"""
import paramiko, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'; PDIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# Check celery error log
print("=== Celery worker error ===")
result = run("cat /var/log/celery/worker.log 2>&1 | tail -30")
print(result[-800:])

print("\n=== Try celery directly ===")
result = run(f"cd {PDIR} && source venv/bin/activate && celery -A yigeworks worker -l info --pidfile=/tmp/celery_test.pid 2>&1 &")
import time; time.sleep(5)
result = run("cat /tmp/celery_test.pid 2>&1 && ps aux | grep celery | grep -v grep | head -5")
print(result)

# Kill test process
run("kill $(cat /tmp/celery_test.pid 2>/dev/null) 2>/dev/null")

ssh.close()
