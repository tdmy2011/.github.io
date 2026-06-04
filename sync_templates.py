"""Download fixed templates from server to local."""
import paramiko, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST = '43.134.232.149'
USER = 'ubuntu'
PASSWORD = 'Yige2026@'
RDIR = '/home/ubuntu/yigeworks_django'
LOCAL_BASE = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)
sftp = ssh.open_sftp()
print('Connected')

templates = [
    'templates/products/product_detail.html',
    'templates/blog/post_detail.html',
    'templates/shop/cart.html',
    'templates/shop/checkout.html',
    'templates/shop/order_success.html',
    'templates/shop/order_list.html',
    'templates/registration/login.html',
    'templates/blog/post_list.html',
    'templates/products/product_list.html',
    'templates/shop/order_detail.html',
]

for rel in templates:
    remote = f'{RDIR}/{rel}'
    local = os.path.join(LOCAL_BASE, rel.replace('/', os.sep))
    try:
        sftp.get(remote, local)
        print(f'  OK: {rel}')
    except Exception as e:
        print(f'  FAIL: {rel} - {e}')

# Also sync settings.py (DEBUG=False)
try:
    sftp.get(f'{RDIR}/yigeworks/settings.py', os.path.join(LOCAL_BASE, 'yigeworks', 'settings.py'))
    print(f'  OK: yigeworks/settings.py')
except Exception as e:
    print(f'  FAIL: settings.py - {e}')

sftp.close()
ssh.close()
print('Done!')
