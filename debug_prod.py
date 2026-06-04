"""Check settings middleware and get real production errors for failing pages."""
import paramiko, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
RDIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
sftp = ssh.open_sftp()
print('Connected')

def run(cmd, label=''):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if label:
        print(f'\n=== {label} ===')
    for line in out.strip().split('\n')[-50:]:
        print(f'  {line}')
    if err.strip() and label:
        print(f'  [STDERR] {err.strip()[:500]}')
    return out, err

# 1. Check middleware in settings
run(f'cat {RDIR}/yigeworks/settings.py 2>&1', 'settings.py')

# 2. Temporarily set DEBUG=True to get error tracebacks
print('\n=== Setting DEBUG=True temporarily ===')
# Read settings, replace DEBUG, upload, test, then restore
out, err = run(f'cat {RDIR}/yigeworks/settings.py')
# Find DEBUG line and replace
lines = out.split('\n')
new_lines = []
for line in lines:
    if line.strip().startswith('DEBUG'):
        new_lines.append('DEBUG = True  # TEMP')
    else:
        new_lines.append(line)
new_content = '\n'.join(new_lines)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write(new_content)
print('  DEBUG=True set')

# Restart Gunicorn
run('sudo systemctl restart yigeworks 2>&1', 'restart gunicorn')
import time; time.sleep(3)

# 3. Get actual error pages
print('\n=== Cart page error ===')
out, err = run('curl -s http://localhost:80/shop/cart/ 2>&1')
# Find the error section in the HTML
import re
error_match = re.search(r'<h1>(.*?)</h1>', out)
if error_match:
    print(f'  Error: {error_match.group(1)}')
# Look for traceback
tb_start = out.find('<pre>')
if tb_start > 0:
    tb = out[tb_start:tb_start+2000]
    for line in tb.split('\n')[:20]:
        print(f'  {line}')

print('\n=== Blog post error ===')
out, err = run('curl -s http://localhost:80/blog/hse-trends-2024/ 2>&1')
error_match = re.search(r'<h1>(.*?)</h1>', out)
if error_match:
    print(f'  Error: {error_match.group(1)}')
tb_start = out.find('<pre>')
if tb_start > 0:
    tb = out[tb_start:tb_start+2000]
    for line in tb.split('\n')[:20]:
        print(f'  {line}')

print('\n=== Product detail (correct URL) ===')
out, err = run('curl -s -o /dev/null -w "%{http_code}" http://localhost:80/products/detail/iso45001-lead-auditor/ 2>&1')
print(f'  Status: {out.strip()}')

# 4. Restore DEBUG=False
print('\n=== Restoring DEBUG=False ===')
lines = new_content.split('\n')
restore_lines = []
for line in lines:
    if line.strip().startswith('DEBUG'):
        restore_lines.append('DEBUG = False')
    else:
        restore_lines.append(line)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write('\n'.join(restore_lines))
run('sudo systemctl restart yigeworks 2>&1', 'restore & restart')

sftp.close()
ssh.close()
print('\nDone!')
