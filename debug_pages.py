"""Debug 3 failing pages: product detail 404, blog post 500, cart 500."""
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
    for line in out.strip().split('\n')[-40:]:
        print(f'  {line}')
    if err.strip() and label:
        print(f'  [STDERR] {err.strip()[:500]}')
    return out, err

# 1. Check URL patterns
print('=== 1. Check URL configs ===')
run(f'cat {RDIR}/products/urls.py 2>&1', 'products/urls.py')
run(f'cat {RDIR}/blog/urls.py 2>&1', 'blog/urls.py')
run(f'cat {RDIR}/shop/urls.py 2>&1', 'shop/urls.py')
run(f'cat {RDIR}/yigeworks/urls.py 2>&1', 'root urls.py')

# 2. Check product slug in DB
print('\n=== 2. Check product slugs ===')
check_slug = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from products.models import Product
for p in Product.objects.all():
    print(f'  slug={p.slug} active={p.is_active}')
'''
with sftp.open(f'{RDIR}/_check.py', 'w') as f:
    f.write(check_slug)
run(f'cd {RDIR} && venv/bin/python _check.py 2>&1', 'product slugs')

# 3. Check blog post slugs
check_blog = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from blog.models import Post
for p in Post.objects.all():
    print(f'  slug={p.slug} status={p.status}')
'''
with sftp.open(f'{RDIR}/_check2.py', 'w') as f:
    f.write(check_blog)
run(f'cd {RDIR} && venv/bin/python _check2.py 2>&1', 'blog slugs')

# 4. Get error details from 500 pages
print('\n=== 3. Get error details ===')
# Enable DEBUG temporarily for error details
run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings DEBUG=1 venv/bin/python manage.py shell -c "pass" 2>&1', 'test debug')

# Set DEBUG=True temporarily, make requests, then set back
debug_script = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from django.test import RequestFactory
from django.conf import settings

# Test cart view
print("--- Cart View ---")
try:
    from shop.views import cart_detail
    rf = RequestFactory()
    req = rf.get('/shop/cart/')
    # Add session
    from django.contrib.sessions.middleware import SessionMiddleware
    middleware = SessionMiddleware(lambda x: x)
    middleware.process_request(req)
    resp = cart_detail(req)
    print(f"Status: {resp.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()

# Test blog post detail
print("\\n--- Blog Post Detail ---")
try:
    from blog.views import post_detail
    rf = RequestFactory()
    req = rf.get('/blog/hse-trends-2024/')
    resp = post_detail(req, slug='hse-trends-2024')
    print(f"Status: {resp.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()

# Test product detail
print("\\n--- Product Detail ---")
try:
    from products.views import product_detail
    rf = RequestFactory()
    req = rf.get('/products/iso45001-lead-auditor/')
    resp = product_detail(req, slug='iso45001-lead-auditor')
    print(f"Status: {resp.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()
'''
with sftp.open(f'{RDIR}/_debug_views.py', 'w') as f:
    f.write(debug_script)
run(f'cd {RDIR} && venv/bin/python _debug_views.py 2>&1', 'debug views')

# 5. Check views source code
run(f'cat {RDIR}/shop/views.py 2>&1', 'shop/views.py')
run(f'cat {RDIR}/blog/views.py 2>&1', 'blog/views.py')
run(f'cat {RDIR}/products/views.py 2>&1', 'products/views.py')

sftp.close()
ssh.close()
print('\nDone!')
