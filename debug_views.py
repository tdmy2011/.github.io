"""获取500错误详情"""
import paramiko, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'; PDIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 用Python直接调用视图获取错误
print("=== Knowledge view error ===")
result = run(f"""cd {PDIR} && source venv/bin/activate && python -c "
import os; os.environ['DJANGO_SETTINGS_MODULE']='yigeworks.settings'
import django; django.setup()
from django.test import RequestFactory
from knowledge.views import knowledge_home
factory = RequestFactory()
request = factory.get('/knowledge/')
try:
    resp = knowledge_home(request)
    print('Status:', resp.status_code)
    print('Content:', str(resp.content)[:500])
except Exception as e:
    print('ERROR:', type(e).__name__, str(e))
" 2>&1""")
print(result)

# 也检查 subscriptions views
print("\n=== Plans view ===")
result = run(f"""cd {PDIR} && source venv/bin/activate && python -c "
import os; os.environ['DJANGO_SETTINGS_MODULE']='yigeworks.settings'
import django; django.setup()
from subscriptions.views import plan_list
from django.test import RequestFactory
factory = RequestFactory()
request = factory.get('/subscriptions/plans/')
try:
    resp = plan_list(request)
    print('Status:', resp.status_code)
except Exception as e:
    print('ERROR:', type(e).__name__, str(e))
" 2>&1""")
print(result)

ssh.close()
