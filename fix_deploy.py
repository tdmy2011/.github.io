import paramiko, sys, io, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'
HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
RDIR = '/home/ubuntu/yigeworks_django'

# Fix any remaining Field_ errors locally
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('venv', 'staticfiles', '__pycache__', '.git', 'media')]
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            fixed = re.sub(r'(models\.\w+Field)_(\()', r'\1\2', content)
            if fixed != content:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(fixed)
                print(f'Fixed: {os.path.relpath(path, BASE)}')

# Connect and deploy
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
sftp = ssh.open_sftp()

# Upload all files
count = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('venv', 'staticfiles', '__pycache__', '.git', 'media')]
    for f in files:
        if f.endswith(('.pyc', '.pyo', '.db', '.DS_Store')):
            continue
        local_path = os.path.join(root, f)
        rel = os.path.relpath(root, BASE).replace('\\', '/')
        if rel == '.':
            remote = f'{RDIR}/{f}'
        else:
            remote = f'{RDIR}/{rel}/{f}'
        try:
            sftp.put(local_path, remote)
            count += 1
        except Exception as e:
            print(f'Error: {rel}/{f}: {e}')
print(f'Uploaded {count} files')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    lines = out.strip().split('\n')
    for line in lines[-5:]:
        print(f'  {line}')
    return out

print('\n=== makemigrations ===')
run(f'cd {RDIR} && venv/bin/python manage.py makemigrations 2>&1')

print('\n=== migrate ===')
run(f'cd {RDIR} && venv/bin/python manage.py migrate 2>&1')

print('\n=== collectstatic ===')
run(f'cd {RDIR} && venv/bin/python manage.py collectstatic --noinput 2>&1')

print('\n=== init_data ===')
run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings venv/bin/python init_data.py 2>&1')

print('\n=== superuser ===')
run(f'cd {RDIR} && venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model;U=get_user_model();print(U.objects.filter(is_superuser=True).count())" 2>&1')

print('\n=== restart + test ===')
ssh.exec_command(f'sudo systemctl restart yigeworks')
time.sleep(3)
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:80/')
code = stdout.read().decode().strip()
print(f'HTTP status: {code}')

stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:80/ 2>&1 | head -5')
print(f'First 5 lines:\n{stdout.read().decode("utf-8", errors="replace")[:500]}')

sftp.close()
ssh.close()
print('\nDone!')
