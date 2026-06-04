"""Diagnose HTTP 502 error on yigeworks Django deployment."""
import paramiko, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
print('Connected to server')

def run_full(cmd):
    """Run command and return full stdout + stderr"""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out, err

def run(cmd, label):
    """Run command and print last N lines"""
    print(f'\n=== {label} ===')
    out, err = run_full(cmd)
    lines = out.strip().split('\n')
    # Print all lines (max 80)
    for line in lines[-80:]:
        print(f'  {line}')
    if err.strip():
        print(f'  [STDERR] {err.strip()[:500]}')
    return out, err

# 1. Gunicorn service status
run('sudo systemctl status yigeworks --no-pager', 'systemctl status yigeworks')

# 2. Gunicorn error logs
run('sudo journalctl -u yigeworks --no-pager -n 50', 'journalctl yigeworks (last 50)')

# 3. Nginx error log
run('sudo tail -30 /var/log/nginx/error.log', 'nginx error.log')

# 4. Nginx site config
run('cat /etc/nginx/sites-enabled/yigeworks 2>/dev/null || cat /etc/nginx/sites-enabled/yigeworks.com 2>/dev/null || echo "NOT FOUND"', 'nginx site config')

# 5. Systemd service file
run('cat /etc/systemd/system/yigeworks.service', 'yigeworks.service')

# 6. Django check
run('cd /home/ubuntu/yigeworks_django && source venv/bin/activate && python manage.py check 2>&1', 'django check')

# 7. Try importing wsgi
run('cd /home/ubuntu/yigeworks_django && source venv/bin/activate && python -c "import yigeworks.wsgi; print(\"WSGI OK\")" 2>&1', 'wsgi import test')

# 8. Check key files exist
run('ls -la /home/ubuntu/yigeworks_django/yigeworks/wsgi.py /home/ubuntu/yigeworks_django/yigeworks/settings.py /home/ubuntu/yigeworks_django/manage.py 2>&1', 'key files check')

# 9. Check Gunicorn is in venv
run('cd /home/ubuntu/yigeworks_django && source venv/bin/activate && which gunicorn && gunicorn --version 2>&1', 'gunicorn check')

# 10. Check database exists
run('ls -la /home/ubuntu/yigeworks_django/db.sqlite3 2>&1', 'database check')

# 11. Try running gunicorn manually to see errors
run('cd /home/ubuntu/yigeworks_django && source venv/bin/activate && timeout 5 gunicorn yigeworks.wsgi:application --bind 0.0.0.0:8000 2>&1 || echo "EXIT CODE: $?"', 'gunicorn manual test')

# 12. Check Nginx listening
run('sudo nginx -t 2>&1', 'nginx config test')

# 13. Check what's listening on port 80 and 8000
run('sudo ss -tlnp | grep -E ":(80|8000)"', 'port listeners')

# 14. Check if staticfiles directory exists
run('ls /home/ubuntu/yigeworks_django/staticfiles/ 2>&1 | head -20', 'staticfiles')

ssh.close()
print('\n=== Diagnosis complete ===')
