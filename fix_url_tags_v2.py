"""Fix incorrect URL names in templates."""
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

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode('utf-8', errors='replace')

def fix_template(path, replacements):
    """Fix URL names in a template file."""
    content = run(f'cat {path}')
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with sftp.open(path, 'w') as f:
            f.write(content)
        changes = []
        for old, new in replacements:
            if old in original:
                changes.append(f'{old} -> {new}')
        print(f'  Fixed: {path.split("templates/")[-1]}')
        for c in changes:
            print(f'    {c}')
        return True
    return False

T = f'{RDIR}/templates'

# 1. cart.html - fix product_list URL and cart_update
print('\n=== 1. Fix cart.html ===')
fix_template(f'{T}/shop/cart.html', [
    ("'shop:product_list'", "'products:list'"),
    ("'shop:cart_update'", "'shop:cart_add'"),  # cart_update doesn't exist, use cart_add
])

# 2. product_detail.html - fix detail URL name
print('\n=== 2. Fix product_detail.html ===')
fix_template(f'{T}/products/product_detail.html', [
    ("'products:product_detail'", "'products:detail'"),
])

# 3. blog/post_detail.html - fix URL names
print('\n=== 3. Fix blog/post_detail.html ===')
fix_template(f'{T}/blog/post_detail.html', [
    ("'blog:post_detail'", "'blog:detail'"),
    ("'blog:post_list'", "'blog:list'"),
])

# 4. checkout.html - fix order_capture URL
print('\n=== 4. Fix checkout.html ===')
fix_template(f'{T}/shop/checkout.html', [
    ("'shop:order_capture'", "'shop:paypal_capture'"),
])

# 5. order_success.html - fix product_list URL
print('\n=== 5. Fix order_success.html ===')
fix_template(f'{T}/shop/order_success.html', [
    ("'shop:product_list'", "'products:list'"),
])

# 6. order_list.html - fix product_list URL
print('\n=== 6. Fix order_list.html ===')
fix_template(f'{T}/shop/order_list.html', [
    ("'shop:product_list'", "'products:list'"),
])

# 7. order_detail.html - check
print('\n=== 7. Check order_detail.html ===')
content = run(f'cat {T}/shop/order_detail.html')
if 'shop:order_list' in content:
    print('  OK: shop:order_list is correct')

# 8. Check base.html for any problematic URLs
print('\n=== 8. Check base.html ===')
content = run(f'cat {T}/base.html')
# Look for any bare product_list, post_list references
for bad in ['product_list', 'post_list', "'cart_detail'"]:
    count = content.count(bad)
    if count > 0:
        print(f'  Found {count} occurrences of "{bad}" in base.html')

# 9. Check if there's a register URL issue
print('\n=== 9. Check registration ===')
content = run(f'cat {T}/registration/login.html')
if "'register'" in content:
    print('  WARNING: register URL not defined, removing link')
    fix_template(f'{T}/registration/login.html', [
        ("{% url 'register' %}", '/accounts/login/'),
    ])

# 10. Verify all pages
print('\n=== 10. Verify all pages ===')
pages = [
    ('/', 'Home'),
    ('/products/', 'Products'),
    ('/products/detail/iso45001-lead-auditor/', 'Product Detail'),
    ('/products/detail/iso14001-lead-auditor/', 'Product 2'),
    ('/blog/', 'Blog'),
    ('/blog/hse-trends-2024/', 'Blog Post'),
    ('/blog/se-asia-compliance/', 'Blog Post 2'),
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
all_ok = True
for path, name in pages:
    out = run(f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:80{path}')
    status = out.strip()
    ok = status in ('200', '302')
    if not ok:
        all_ok = False
    icon = 'OK' if ok else 'FAIL'
    print(f'  [{icon}] {name:20s} {path:50s} -> {status}')

if all_ok:
    print('\n  >>> ALL PAGES OK! <<<')
else:
    print('\n  Some pages still failing.')

sftp.close()
ssh.close()
print('\nDone!')
