"""
检查 chapter11 中是否存在 form.py, pays_new.py 等缺失文件
"""
import paramiko

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
SRC = '/home/ubuntu/django3web_src/extracted/chapter11/babys'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER, username=USER, password=PASS, timeout=15)

def cat(path):
    stdin, stdout, stderr = ssh.exec_command(f'cat {path}', timeout=15)
    return stdout.read().decode('utf-8', errors='replace')

# Check shopper directory for all files
stdin, stdout, stderr = ssh.exec_command(f'find {SRC}/shopper -type f | grep -v __pycache__ | sort', timeout=15)
print("=== shopper files ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check all directories for form.py and pays_new.py
stdin, stdout, stderr = ssh.exec_command(f'find {SRC} -name "form.py" -o -name "pays_new.py" -o -name "form*.py" -o -name "pay*.py" 2>/dev/null', timeout=15)
print("=== form/pay files ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check all .py files in shopper
stdin, stdout, stderr = ssh.exec_command(f'find {SRC}/shopper -name "*.py" -type f | grep -v __pycache__ | sort', timeout=15)
print("=== all .py in shopper ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Read form.py if exists
for fn in ['form.py', 'pays_new.py', 'forms.py', 'pay.py']:
    path = f'{SRC}/shopper/{fn}'
    stdin, stdout, stderr = ssh.exec_command(f'test -f {path} && cat {path}', timeout=15)
    content = stdout.read().decode('utf-8', errors='replace')
    if content.strip():
        print(f"\n=== {fn} ===")
        print(content)

ssh.close()
