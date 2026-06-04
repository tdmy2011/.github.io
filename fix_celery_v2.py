"""修复Celery systemd服务"""
import paramiko, sys, time
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
sftp = ssh.open_sftp()

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# Kill existing test process
run("pkill -f 'celery.*worker' 2>/dev/null")
run("pkill -f 'celery.*beat' 2>/dev/null")
time.sleep(2)

# Fix log dir
run("sudo mkdir -p /var/log/celery && sudo chown -R ubuntu:ubuntu /var/log/celery")
run("sudo mkdir -p /var/run/celery && sudo chown -R ubuntu:ubuntu /var/run/celery")

# Write fixed worker service - use simple type instead of forking
worker_service = """[Unit]
Description=Celery Worker for YigeWorks
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="DJANGO_SETTINGS_MODULE=yigeworks.settings"
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/celery -A yigeworks worker -l info --pidfile=/var/run/celery/worker.pid --logfile=/var/log/celery/worker.log
ExecStop=/bin/kill -s TERM $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target"""

beat_service = """[Unit]
Description=Celery Beat for YigeWorks
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/yigeworks_django
Environment="PATH=/home/ubuntu/yigeworks_django/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="DJANGO_SETTINGS_MODULE=yigeworks.settings"
ExecStart=/home/ubuntu/yigeworks_django/venv/bin/celery -A yigeworks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile=/var/run/celery/beat.pid --logfile=/var/log/celery/beat.log

[Install]
WantedBy=multi-user.target"""

# Write service files via SFTP
with sftp.file('/tmp/celery-worker.service', 'w') as f:
    f.write(worker_service)
with sftp.file('/tmp/celery-beat.service', 'w') as f:
    f.write(beat_service)

run("sudo cp /tmp/celery-worker.service /etc/systemd/system/")
run("sudo cp /tmp/celery-beat.service /etc/systemd/system/")
run("sudo systemctl daemon-reload")
run("sudo systemctl enable celery-worker celery-beat")
run("sudo systemctl start celery-worker celery-beat")
time.sleep(5)

# Verify
print("=== Celery Worker ===")
result = run("sudo systemctl status celery-worker --no-pager 2>&1")
for line in result.split('\n')[:5]:
    print(line)

print("\n=== Celery Beat ===")
result = run("sudo systemctl status celery-beat --no-pager 2>&1")
for line in result.split('\n')[:5]:
    print(line)

# Verify processes
print("\n=== Running processes ===")
result = run("ps aux | grep celery | grep -v grep")
for line in result.split('\n')[:6]:
    print(line)

sftp.close()
ssh.close()
