"""Fix ServiceRegion data and verify all pages."""
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
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if label:
        print(f'\n=== {label} ===')
    for line in out.strip().split('\n')[-30:]:
        print(f'  {line}')
    if err.strip() and label:
        print(f'  [STDERR] {err.strip()[:500]}')
    return out, err

# Fix ServiceRegion + create remaining data
fix_script = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from pages.models import ServiceRegion

regions = [
    ('越南 Vietnam', '越南', 'Vietnam', 'southeast_asia', '劳动安全法', 'ISO认证,安全培训,风险评估'),
    ('泰国 Thailand', '泰国', 'Thailand', 'southeast_asia', '泰国安全法规', 'ISO认证,安全培训,合规咨询'),
    ('印尼 Indonesia', '印尼', 'Indonesia', 'southeast_asia', 'SMK3法规', 'ISO认证,安全培训,风险评估'),
    ('马来西亚 Malaysia', '马来西亚', 'Malaysia', 'southeast_asia', 'OSHA 1994', 'ISO认证,合规咨询'),
    ('菲律宾 Philippines', '菲律宾', 'Philippines', 'southeast_asia', 'DOLE法规', '安全培训,合规咨询'),
    ('缅甸 Myanmar', '缅甸', 'Myanmar', 'southeast_asia', '工厂法', '安全培训'),
    ('柬埔寨 Cambodia', '柬埔寨', 'Cambodia', 'southeast_asia', '劳动法', '安全培训'),
    ('老挝 Laos', '老挝', 'Laos', 'southeast_asia', '劳动法', '安全培训'),
    ('新加坡 Singapore', '新加坡', 'Singapore', 'southeast_asia', 'WSH法案', 'ISO认证,安全培训'),
    ('尼日利亚 Nigeria', '尼日利亚', 'Nigeria', 'africa', 'NIOSH法规', 'ISO认证,安全培训'),
    ('肯尼亚 Kenya', '肯尼亚', 'Kenya', 'africa', 'OSHA法案', '安全培训,合规咨询'),
    ('坦桑尼亚 Tanzania', '坦桑尼亚', 'Tanzania', 'africa', 'OSHA法规', '安全培训'),
    ('埃塞俄比亚 Ethiopia', '埃塞俄比亚', 'Ethiopia', 'africa', '劳动法', '安全培训'),
    ('加纳 Ghana', '加纳', 'Ghana', 'africa', '工厂法', '安全培训'),
    ('南非 South Africa', '南非', 'South Africa', 'africa', 'OHSA法案', 'ISO认证,安全培训,风险评估'),
    ('中国大陆 China', '中国大陆', 'China', 'greater_china', '安全生产法', 'ISO认证,安全培训,风险评估,合规咨询'),
    ('香港 Hong Kong', '香港', 'Hong Kong', 'greater_china', '工厂及工业经营条例', '安全培训,风险评估'),
]
for label, name_zh, name_en, region, regulations, services in regions:
    r, cr = ServiceRegion.objects.get_or_create(
        name_zh=name_zh, name_en=name_en,
        defaults={'region_type': region, 'regulations': regulations, 'services': services, 'is_active': True}
    )
    print(f'  Region: {name_zh} {"created" if cr else "exists"}')

print(f'Total ServiceRegions: {ServiceRegion.objects.count()}')
'''

with sftp.open(f'{RDIR}/_fix_regions.py', 'w') as f:
    f.write(fix_script)
print('Uploaded _fix_regions.py')

run(f'cd {RDIR} && venv/bin/python _fix_regions.py 2>&1', 'fix regions')

# Verify all pages
print('\n=== Page Test ===')
pages = [
    ('/', 'Home'),
    ('/products/', 'Products'),
    ('/products/iso45001-lead-auditor/', 'Product Detail'),
    ('/blog/', 'Blog'),
    ('/blog/hse-trends-2024/', 'Blog Post'),
    ('/contact/', 'Contact'),
    ('/global/', 'Global'),
    ('/pricing/', 'Pricing'),
    ('/course/', 'Course'),
    ('/privacy/', 'Privacy'),
    ('/terms/', 'Terms'),
    ('/shop/cart/', 'Cart'),
    ('/admin/', 'Admin Login'),
]
for path, name in pages:
    out, err = run(f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:80{path}')
    status = out.strip()
    icon = 'OK' if status in ('200', '302') else 'FAIL'
    print(f'  [{icon}] {name:20s} {path:40s} -> {status}')

# Final data counts
print('\n=== Final Data Counts ===')
count_script = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from pages.models import SiteConfig, FAQ, ServiceRegion
from products.models import Category, Product
from blog.models import PostCategory, Post, Tag
from django.contrib.auth import get_user_model
print(f'SiteConfig: {SiteConfig.objects.count()}')
print(f'FAQ: {FAQ.objects.count()}')
print(f'ServiceRegion: {ServiceRegion.objects.count()}')
print(f'Category: {Category.objects.count()}')
print(f'Product: {Product.objects.count()}')
print(f'PostCategory: {PostCategory.objects.count()}')
print(f'Post: {Post.objects.count()}')
print(f'Tag: {Tag.objects.count()}')
print(f'Superuser: {get_user_model().objects.filter(is_superuser=True).count()}')
'''

with sftp.open(f'{RDIR}/_count.py', 'w') as f:
    f.write(count_script)
run(f'cd {RDIR} && venv/bin/python _count.py 2>&1', 'data counts')

sftp.close()
ssh.close()
print('\nDone!')
