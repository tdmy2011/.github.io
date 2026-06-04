"""Complete deployment: init data + create superuser + verify admin."""
import paramiko, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
RDIR = '/home/ubuntu/yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
print('Connected')

def run(cmd, label=''):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if label:
        print(f'\n=== {label} ===')
    for line in out.strip().split('\n')[-20:]:
        print(f'  {line}')
    if err.strip() and label:
        print(f'  [STDERR] {err.strip()[:300]}')
    return out, err

# 1. Run init_data.py with full DJANGO_SETTINGS_MODULE
print('Running init_data.py...')
run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings venv/bin/python init_data.py 2>&1', 'init_data')

# 2. Create superuser
print('\nCreating superuser...')
out, err = run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings venv/bin/python -c "'
    'import django; django.setup();'
    'from django.contrib.auth import get_user_model;'
    'User = get_user_model();'
    'if not User.objects.filter(username=\"admin\").exists():'
    '    User.objects.create_superuser(\"admin\", \"yjurado860@gmail.com\", \"Yige2026@\");'
    '    print(\"Superuser created: admin\");'
    'else:'
    '    print(\"Superuser already exists\");'
    '" 2>&1', 'create superuser')

# 3. Verify data counts
print('\nVerifying data...')
run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings venv/bin/python -c "'
    'import django; django.setup();'
    'from pages.models import SiteConfig, HeroBanner, FAQ, Testimonial, ServiceRegion;'
    'from products.models import Category, Product;'
    'from blog.models import PostCategory, Post, Tag;'
    'from inquiries.models import ContactInquiry, Subscriber;'
    'from shop.models import Order;'
    'from django.contrib.auth import get_user_model;'
    'print(f\"SiteConfig: {SiteConfig.objects.count()}\");'
    'print(f\"HeroBanner: {HeroBanner.objects.count()}\");'
    'print(f\"FAQ: {FAQ.objects.count()}\");'
    'print(f\"Testimonial: {Testimonial.objects.count()}\");'
    'print(f\"ServiceRegion: {ServiceRegion.objects.count()}\");'
    'print(f\"Category: {Category.objects.count()}\");'
    'print(f\"Product: {Product.objects.count()}\");'
    'print(f\"PostCategory: {PostCategory.objects.count()}\");'
    'print(f\"Tag: {Tag.objects.count()}\");'
    'print(f\"Post: {Post.objects.count()}\");'
    'print(f\"User (superuser): {get_user_model().objects.filter(is_superuser=True).count()}\");'
    'print(f\"Order: {Order.objects.count()}\");'
    '" 2>&1', 'data counts')

# 4. Test key pages
print('\nTesting pages...')
for path in ['/', '/products/', '/blog/', '/contact/', '/global/', '/pricing/', '/course/',
             '/shop/cart/', '/admin/']:
    out, err = run(f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:80{path} 2>&1')
    print(f'  {path} -> HTTP {out.strip()}')

ssh.close()
print('\nDone!')
