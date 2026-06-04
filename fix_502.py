"""Fix Gunicorn socket permission - Nginx (www-data) can't access socket created by ubuntu user."""
import paramiko, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
print('Connected')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out.strip(), err.strip()

# Fix: Add www-data to ubuntu group so Nginx can access the socket
print('\n=== 1. Add www-data to ubuntu group ===')
out, err = run('sudo usermod -aG www-data ubuntu 2>&1')
print(f'  {out or "OK"}')
if err: print(f'  [ERR] {err}')

# Fix: Update Gunicorn service to use RuntimeDirectory in /run/gunicorn
# and set socket permissions properly
print('\n=== 2. Update systemd service file ===')
service_content = '''[Unit]
Description=YigeWorks Django Gunicorn
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin"
ExecStartPre=/bin/rm -f /run/gunicorn/yigeworks.sock
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/gunicorn \\
    --bind unix:/run/gunicorn/yigeworks.sock \\
    --workers 3 \\
    --timeout 120 \\
    yigeworks.wsgi:application
ExecStartPost=/bin/chmod 666 /run/gunicorn/yigeworks.sock
RuntimeDirectory=gunicorn
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target'''

sftp = ssh.open_sftp()
# Write service file to temp location
with sftp.open('/tmp/yigeworks.service', 'w') as f:
    f.write(service_content)

out, err = run('sudo cp /tmp/yigeworks.service /etc/systemd/system/yigeworks.service 2>&1')
print(f'  Copy: {out or "OK"}')
if err: print(f'  [ERR] {err}')

# Also update Nginx config to point to new socket path
print('\n=== 3. Update Nginx config ===')
nginx_conf = '''server {
    listen 80;
    server_name yigeworks.com www.yigeworks.com 43.134.232.149;

    client_max_body_size 50M;

    location /static/ {
        alias /home/ubuntu/yigeworks_django/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/ubuntu/yigeworks_django/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn/yigeworks.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}'''

with sftp.open('/tmp/yigeworks_nginx', 'w') as f:
    f.write(nginx_conf)

out, err = run('sudo cp /tmp/yigeworks_nginx /etc/nginx/sites-enabled/yigeworks 2>&1')
print(f'  Copy: {out or "OK"}')
if err: print(f'  [ERR] {err}')

# Remove old socket if exists
print('\n=== 4. Clean up old socket ===')
out, err = run('rm -f /home/ubuntu/yigeworks_django/gunicorn.sock 2>&1')
print(f'  {out or "Cleaned"}')

# Reload systemd daemon
print('\n=== 5. Reload systemd + restart ===')
out, err = run('sudo systemctl daemon-reload 2>&1')
print(f'  daemon-reload: {out or "OK"}')
if err: print(f'  [ERR] {err}')

out, err = run('sudo systemctl restart yigeworks 2>&1')
print(f'  restart: {out or "OK"}')
if err: print(f'  [ERR] {err}')

# Restart nginx
print('\n=== 6. Restart Nginx ===')
out, err = run('sudo systemctl restart nginx 2>&1')
print(f'  restart: {out or "OK"}')
if err: print(f'  [ERR] {err}')

time.sleep(3)

# Test
print('\n=== 7. Test HTTP ===')
out, err = run('curl -s -o /dev/null -w "%{http_code}" http://localhost:80/')
print(f'  HTTP status: {out}')

out, err = run('curl -s http://localhost:80/ 2>&1 | head -10')
print(f'  Response:\n{out[:1000]}')

# Check service status
print('\n=== 8. Service status ===')
out, err = run('sudo systemctl status yigeworks --no-pager 2>&1')
for line in out.split('\n')[:15]:
    print(f'  {line}')

sftp.close()
ssh.close()
print('\nDone!')
