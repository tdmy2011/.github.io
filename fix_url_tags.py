"""Find and fix all URL tags in templates that need app namespace prefix."""
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

# 1. Find all url tags in templates
print('\n=== 1. Finding all {% url %} tags ===')
out = run(f'cd {RDIR} && grep -rn "{{% url" templates/ 2>/dev/null')
if out.strip():
    for line in out.strip().split('\n'):
        print(f'  {line}')
else:
    print('  No url tags found')

# 2. Check what URL names are defined in each app
print('\n=== 2. URL names per app ===')
for app, url_file in [('products', 'products/urls.py'), ('blog', 'blog/urls.py'),
                      ('shop', 'shop/urls.py'), ('inquiries', 'inquiries/urls.py'),
                      ('pages', 'pages/urls.py')]:
    content = run(f'cat {RDIR}/{url_file} 2>/dev/null')
    names = re.findall(r"name='(\w+)'", content)
    app_name = re.search(r"app_name = '(\w+)'", content)
    prefix = app_name.group(1) if app_name else '(no app_name)'
    print(f'  {app} ({prefix}): {names}')

# 3. Fix all templates
print('\n=== 3. Fixing URL tags ===')

# URL name mapping: bare name -> namespaced name
url_fixes = {
    # products app
    "'product_list'": "'products:list'",
    "'product_detail'": "'products:detail'",
    "'product_category'": "'products:category'",
    # blog app
    "'post_list'": "'blog:list'",
    "'post_detail'": "'blog:detail'",
    "'blog_category'": "'blog:category'",
    # shop app
    "'cart_detail'": "'shop:cart'",
    "'cart_add'": "'shop:cart_add'",
    "'cart_remove'": "'shop:cart_remove'",
    "'cart_clear'": "'shop:cart_clear'",
    "'checkout'": "'shop:checkout'",
    "'create_order'": "'shop:order_create'",
    "'order_success'": "'shop:order_success'",
    "'order_list'": "'shop:order_list'",
    "'order_detail'": "'shop:order_detail'",
    # inquiries app (check first)
    # pages app
}

# List all template files
out = run(f'find {RDIR}/templates -name "*.html" 2>/dev/null')
template_files = [f.strip() for f in out.strip().split('\n') if f.strip()]

fix_count = 0
for template_path in template_files:
    content = run(f'cat {template_path}')
    original = content
    
    for old_name, new_name in url_fixes.items():
        content = content.replace(old_name, new_name)
    
    if content != original:
        with sftp.open(template_path, 'w') as f:
            f.write(content)
        fix_count += 1
        rel = template_path.replace(f'{RDIR}/templates/', '')
        # Count what was changed
        changes = set()
        for old_name in url_fixes:
            if old_name in original:
                changes.add(f'{old_name}->{url_fixes[old_name]}')
        print(f'  Fixed: {rel} ({", ".join(changes)})')

print(f'\nTotal files fixed: {fix_count}')

# 4. Verify all pages again
print('\n=== 4. Verify all pages ===')
pages = [
    ('/', 'Home'),
    ('/products/', 'Products'),
    ('/products/detail/iso45001-lead-auditor/', 'Product Detail'),
    ('/blog/', 'Blog'),
    ('/blog/hse-trends-2024/', 'Blog Post'),
    ('/contact/', 'Contact'),
    ('/global/', 'Global'),
    ('/pricing/', 'Pricing'),
    ('/course/', 'Course'),
    ('/privacy/', 'Privacy'),
    ('/terms/', 'Terms'),
    ('/shop/cart/', 'Cart'),
    ('/shop/checkout/', 'Checkout'),
    ('/admin/', 'Admin'),
]
for path, name in pages:
    out = run(f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:80{path}')
    status = out.strip()
    icon = 'OK' if status in ('200', '302') else 'FAIL'
    print(f'  [{icon}] {name:20s} {path:45s} -> {status}')

sftp.close()
ssh.close()
print('\nDone!')
