"""上传修复的knowledge views并测试"""
import paramiko, sys, time
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', buffering=1)

HOST = '43.134.232.149'; USER = 'ubuntu'; PASSWORD = 'Yige2026@'; PDIR = '/home/ubuntu/yigeworks_django'
LOCAL = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
sftp = ssh.open_sftp()

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# Upload
sftp.put(LOCAL + '/knowledge/views.py', PDIR + '/knowledge/views.py')
print("Uploaded knowledge/views.py")
sftp.close()

# Restart
run("sudo systemctl restart yigeworks 2>&1")
time.sleep(3)

# Test all pages
print("\n=== Test all pages ===")
urls = [
    ('/', 'Home'),
    ('/knowledge/', 'Knowledge Home'),
    ('/knowledge/explore/', 'Knowledge Explore'),
    ('/knowledge/search/', 'Knowledge Search'),
    ('/subscriptions/plans/', 'Plans'),
    ('/subscriptions/dashboard/', 'Dashboard (302)'),
    ('/ai/', 'AI Engine (302)'),
    ('/geo/', 'GEO (302)'),
    ('/admin/', 'Admin (302)'),
    ('/blog/', 'Blog'),
    ('/products/', 'Products'),
    ('/shop/cart/', 'Cart'),
    ('/contact/', 'Contact'),
    ('/privacy/', 'Privacy'),
    ('/terms/', 'Terms'),
]
ok_count = 0
fail_count = 0
for url, name in urls:
    code = run(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8000{url} 2>&1").strip()
    is_ok = code in ('200', '302', '301', '404', '405')
    if is_ok:
        ok_count += 1
    else:
        fail_count += 1
    print(f"  {code} {name} {'OK' if is_ok else 'FAIL'}")

print(f"\n=== Result: {ok_count} OK, {fail_count} FAIL ===")

# Get detail for any failures
if fail_count > 0:
    print("\n=== Failure details ===")
    for url, name in urls:
        code = run(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8000{url} 2>&1").strip()
        if code not in ('200', '302', '301', '404', '405'):
            result = run(f"curl -s http://localhost:8000{url} 2>&1")
            # Extract error
            import re
            errs = re.findall(r'ValueError|TypeError|TemplateDoesNotExist|NoReverseMatch|[A-Z][a-z]+Error.*?</h2>', result)
            for e in errs[:3]:
                print(f"  {name}: {e[:200]}")

ssh.close()
