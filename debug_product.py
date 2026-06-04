"""Completely fix product detail template image handling."""
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

# First, let me see the CURRENT state of product_detail.html
print('\n=== Current product_detail.html ===')
content = run(f'cat {RDIR}/templates/products/product_detail.html')
for i, line in enumerate(content.split('\n'), 1):
    print(f'  {i:3d}: {line}')

# Get the actual error
print('\n=== Get exact error ===')
# Set DEBUG
settings = run(f'cat {RDIR}/yigeworks/settings.py')
lines = settings.split('\n')
new_lines = []
for line in lines:
    if line.strip().startswith('DEBUG'):
        new_lines.append('DEBUG = True')
    else:
        new_lines.append(line)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write('\n'.join(new_lines))
run('sudo systemctl restart yigeworks 2>&1')
import time; time.sleep(3)

out = run('curl -s http://localhost:80/products/detail/iso45001-lead-auditor/ 2>&1')
# Find the exception
exc = re.search(r"<h1>(.*?)</h1>", out)
if exc: print(f'  Exception: {exc.group(1)}')
loc = re.search(r"Exception Location:</th>\s*<td>(.*?)</td>", out)
if loc: print(f'  Location: {loc.group(1)}')
msg = re.search(r"<pre>(.*?)</pre>", out)
if msg:
    error_text = re.sub(r'<[^>]+>', '', msg.group(1)).strip()
    print(f'  Error text: {error_text[:500]}')

# Get more context around the error
# Look for the traceback
tb_section = re.search(r'<tbody>(.*?)</tbody>', out, re.DOTALL)
if tb_section:
    for frame_match in re.finditer(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>', tb_section.group(1)):
        file_info = frame_match.group(1).strip()
        code_info = re.sub(r'<[^>]+>', '', frame_match.group(2)).strip()
        if 'yigeworks' in file_info or 'templates' in file_info:
            print(f'  Frame: {file_info} | {code_info[:100]}')

sftp.close()
ssh.close()
print('\nDone!')
