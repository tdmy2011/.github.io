"""获取详细错误信息"""
import paramiko, sys, time
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'; PDIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 1. Run migrations with full output
print("=== makemigrations full ===")
result = run(f"cd {PDIR} && source venv/bin/activate && DJANGO_SETTINGS_MODULE=yigeworks.settings python manage.py makemigrations knowledge subscriptions ai_engine email_campaigns geo_analytics 2>&1")
for line in result.split('\n'):
    if 'Migrat' in line or 'Error' in line or 'Traceback' in line or '.py' in line:
        print(line)

print("\n=== migrate full ===")
result = run(f"cd {PDIR} && source venv/bin/activate && python manage.py migrate 2>&1")
for line in result.split('\n'):
    if 'Migrat' in line or 'Error' in line or 'Running' in line or 'Applying' in line or 'OK' in line:
        print(line)

# 2. Knowledge 500 error
print("\n=== Knowledge 500 error ===")
result = run("curl -s http://localhost:8000/knowledge/ 2>&1")
# Show last 500 chars
print(result[-500:] if len(result) > 500 else result)

# 3. Check if tables exist
print("\n=== Check tables ===")
result = run(f"cd {PDIR} && source venv/bin/activate && python -c \"\nimport os; os.environ['DJANGO_SETTINGS_MODULE']='yigeworks.settings'\nimport django; django.setup()\nfrom django.db import connection\ncursor = connection.cursor()\ncursor.execute(\\\"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'knowledge%' OR name LIKE 'subscript%' ORDER BY name\\\")\nfor row in cursor.fetchall(): print(row[0])\n\" 2>&1")
print(result)

ssh.close()
