"""Fix image-related errors and check blog post 2."""
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

# 1. Check product_detail.html for image references
print('\n=== 1. Product detail template ===')
content = run(f'cat {RDIR}/templates/products/product_detail.html')
# Find all image references
for i, line in enumerate(content.split('\n'), 1):
    if 'image' in line.lower() or 'img' in line.lower():
        print(f'  L{i}: {line.strip()[:100]}')

# Fix: wrap image access in {% if %} blocks
print('\n=== 2. Fix product_detail.html ===')
# Read full content and add if guards
content = run(f'cat {RDIR}/templates/products/product_detail.html')

# Replace {{ product.image.url }} with conditional
content = content.replace(
    '<img src="{{ product.image.url }}"',
    '{% if product.image %}<img src="{{ product.image.url }}"'
)
# Close the if block after the img tag - need to find the end
# Simple approach: wrap in if/endif
content = content.replace(
    '{% if product.image %}<img src="{{ product.image.url }}"',
    '{% if product.image %}\n            <img src="{{ product.image.url }}"'
)

# Also fix any product.file references
content = content.replace(
    'href="{{ product.file.url }}"',
    '{% if product.file %}href="{{ product.file.url }}"{% endif %}'
)

with sftp.open(f'{RDIR}/templates/products/product_detail.html', 'w') as f:
    f.write(content)
print('  Added {% if product.image %} guard')

# 3. Check blog post_detail.html for image references
print('\n=== 3. Blog post detail template ===')
content = run(f'cat {RDIR}/templates/blog/post_detail.html')
for i, line in enumerate(content.split('\n'), 1):
    if 'image' in line.lower() or 'img' in line.lower():
        print(f'  L{i}: {line.strip()[:100]}')

# Fix blog post_detail.html too
content = content.replace(
    '<img src="{{ post.cover_image.url }}"',
    '{% if post.cover_image %}<img src="{{ post.cover_image.url }}"'
)

with sftp.open(f'{RDIR}/templates/blog/post_detail.html', 'w') as f:
    f.write(content)
print('  Added {% if post.cover_image %} guard')

# 4. Check blog post list template for image references
print('\n=== 4. Blog list template ===')
content = run(f'cat {RDIR}/templates/blog/post_list.html')
for i, line in enumerate(content.split('\n'), 1):
    if 'image' in line.lower() or 'img' in line.lower() or 'cover' in line.lower():
        print(f'  L{i}: {line.strip()[:100]}')

# Fix blog list template too if it has image references
if 'cover_image' in content:
    content = content.replace(
        '{{ post.cover_image.url }}',
        '{% if post.cover_image %}{{ post.cover_image.url }}{% endif %}'
    )
    with sftp.open(f'{RDIR}/templates/blog/post_list.html', 'w') as f:
        f.write(content)
    print('  Fixed cover_image reference')

# 5. Check product list template
print('\n=== 5. Product list template ===')
content = run(f'cat {RDIR}/templates/products/product_list.html')
for i, line in enumerate(content.split('\n'), 1):
    if 'image' in line.lower() or 'img' in line.lower():
        print(f'  L{i}: {line.strip()[:100]}')

if 'product.image.url' in content:
    content = content.replace(
        '{{ product.image.url }}',
        '{% if product.image %}{{ product.image.url }}{% endif %}'
    )
    with sftp.open(f'{RDIR}/templates/products/product_list.html', 'w') as f:
        f.write(content)
    print('  Fixed product.image.url reference')

# 6. Verify all pages
print('\n=== 6. Verify all pages ===')
pages = [
    ('/', 'Home'),
    ('/products/', 'Products'),
    ('/products/detail/iso45001-lead-auditor/', 'Product Detail 1'),
    ('/products/detail/iso14001-lead-auditor/', 'Product Detail 2'),
    ('/products/detail/safety-manual-template/', 'Product Detail 3'),
    ('/blog/', 'Blog'),
    ('/blog/hse-trends-2024/', 'Blog 1'),
    ('/blog/se-asia-compliance/', 'Blog 2'),
    ('/blog/iso-certification-guide/', 'Blog 3'),
    ('/blog/safety-culture-build/', 'Blog 4'),
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

sftp.close()
ssh.close()
print('\nDone!')
