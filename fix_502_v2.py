"""Fix 502: Switch Gunicorn to TCP binding (localhost:8000) to avoid socket permission issues."""
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

# 1. Update systemd service: use TCP localhost:8000
print('\n=== 1. Update systemd service (TCP bind) ===')
service_content = '''[Unit]
Description=YigeWorks Django Gunicorn
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin"
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/gunicorn \\
    --bind 127.0.0.1:8000 \\
    --workers 3 \\
    --timeout 120 \\
    yigeworks.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target'''

sftp = ssh.open_sftp()
with sftp.open('/tmp/yigeworks.service', 'w') as f:
    f.write(service_content)

out, err = run('sudo cp /tmp/yigeworks.service /etc/systemd/system/yigeworks.service 2>&1')
print(f'  Copy: {out or "OK"}')

# 2. Update Nginx config: proxy to TCP instead of socket
print('\n=== 2. Update Nginx config ===')
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
        proxy_pass http://127.0.0.1:8000;
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

# 3. Test nginx config
print('\n=== 3. Test Nginx config ===')
out, err = run('sudo nginx -t 2>&1')
print(f'  {out}')

# 4. Reload + restart
print('\n=== 4. Reload systemd + restart services ===')
out, err = run('sudo systemctl daemon-reload 2>&1')
print(f'  daemon-reload: {out or "OK"}')

out, err = run('sudo systemctl restart yigeworks 2>&1')
print(f'  restart yigeworks: {out or "OK"}')

out, err = run('sudo systemctl restart nginx 2>&1')
print(f'  restart nginx: {out or "OK"}')

time.sleep(3)

# 5. Test
print('\n=== 5. Service status ===')
out, err = run('sudo systemctl status yigeworks --no-pager 2>&1')
for line in out.split('\n')[:12]:
    print(f'  {line}')

print('\n=== 6. Test HTTP ===')
out, err = run('curl -s -o /dev/null -w "%{http_code}" http://localhost:80/')
print(f'  HTTP status: {out}')

out, err = run('curl -s http://localhost:80/ 2>&1 | head -15')
for line in out.split('\n')[:15]:
    print(f'  {line}')

# 7. External test
print('\n=== 7. External test ===')
out, err = run('curl -s -o /dev/null -w "%{http_code}" http://43.134.232.149/ 2>&1')
print(f'  External HTTP status: {out}')

out, err = run('curl -s http://43.134.232.149/ 2>&1 | head -5')
print(f'  First 5 lines:\n{out[:500]}')

sftp.close()
ssh.close()
print('\nDone!')
