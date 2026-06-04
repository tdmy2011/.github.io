"""Get exact errors for remaining 500 pages."""
import paramiko, sys, io, re

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

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace')

# Enable DEBUG
out = run(f'cat {RDIR}/yigeworks/settings.py')
lines = out.split('\n')
new_lines = []
for line in lines:
    if line.strip().startswith('DEBUG'):
        new_lines.append('DEBUG = True  # TEMP')
    else:
        new_lines.append(line)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write('\n'.join(new_lines))

run('sudo systemctl restart yigeworks 2>&1')
import time; time.sleep(3)

# Test product detail
print('\n=== Product Detail Error ===')
out = run('curl -s http://localhost:80/products/detail/iso45001-lead-auditor/ 2>&1')
# Find exception type and message
exc = re.search(r"<h1>(.*?)</h1>", out)
if exc: print(f'  Exception: {exc.group(1)}')
loc = re.search(r"Exception Location:</th>\s*<td>(.*?)</td>", out)
if loc: print(f'  Location: {loc.group(1)}')
msg = re.search(r"<pre>(.*?)</pre>", out)
if msg: 
    error_text = re.sub(r'<[^>]+>', '', msg.group(1))
    print(f'  Error: {error_text[:300]}')

# Test blog post 2
print('\n=== Blog Post 2 Error ===')
out = run('curl -s http://localhost:80/blog/se-asia-compliance/ 2>&1')
exc = re.search(r"<h1>(.*?)</h1>", out)
if exc: print(f'  Exception: {exc.group(1)}')
loc = re.search(r"Exception Location:</th>\s*<td>(.*?)</td>", out)
if loc: print(f'  Location: {loc.group(1)}')
msg = re.search(r"<pre>(.*?)</pre>", out)
if msg:
    error_text = re.sub(r'<[^>]+>', '', msg.group(1))
    print(f'  Error: {error_text[:300]}')

# Restore DEBUG=False
lines = new_lines
restore = []
for line in lines:
    if 'DEBUG = True  # TEMP' in line:
        restore.append('DEBUG = False')
    else:
        restore.append(line)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write('\n'.join(restore))
run('sudo systemctl restart yigeworks 2>&1')

sftp.close()
ssh.close()
print('\nDone!')
