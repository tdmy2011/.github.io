"""
集成 Django3-Web 源码到 yigeworks 项目（修复版）
"""
import paramiko
import os
import shutil

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
SRC = '/home/ubuntu/django3web_src/extracted/chapter11/babys'
PROJECT = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

APP_MAP = {
    'index': 'book_index',
    'commodity': 'book_commodity',
    'shopper': 'book_shopper',
}

def ssh_cmd(ssh, cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read()
    err = stderr.read()
    try:
        return out.decode('utf-8', errors='replace'), err.decode('utf-8', errors='replace')
    except:
        return out.decode('gbk', errors='replace'), err.decode('gbk', errors='replace')

def sftp_download(sftp, remote_path, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    sftp.get(remote_path, local_path)

def fix_gbk(raw_bytes):
    try:
        text = raw_bytes.decode('utf-8')
        if '\ufffd' not in text:
            return text
    except:
        pass
    try:
        return raw_bytes.decode('gbk', errors='replace')
    except:
        return raw_bytes.decode('utf-8', errors='replace')

def fix_code_references(text):
    """Fix all import and URL references for renamed apps"""
    text = text.replace('from commodity.models import', 'from book_commodity.models import')
    text = text.replace('from commodity.views import', 'from book_commodity.views import')
    text = text.replace("include('commodity.urls')", "include('book_commodity.urls')")
    text = text.replace("include('shopper.urls')", "include('book_shopper.urls')")
    text = text.replace("include('index.urls')", "include('book_index.urls')")
    return text

def fix_template_references(text):
    """Fix template URL and static references"""
    if "{% extends 'base.html' %}" in text:
        text = text.replace("{% extends 'base.html' %}", "{% extends 'book/base.html' %}")
    text = text.replace("{% url 'index:", "{% url 'book_index:")
    text = text.replace("{% url 'commodity:", "{% url 'book_commodity:")
    text = text.replace("{% url 'shopper:", "{% url 'book_shopper:")
    text = text.replace("{% static 'css/", "{% static 'book/css/")
    text = text.replace("{% static 'js/", "{% static 'book/js/")
    text = text.replace("{% static 'img/", "{% static 'book/img/")
    text = text.replace("{% static 'layui/", "{% static 'book/layui/")
    text = text.replace("{% static 'font/", "{% static 'book/font/")
    text = text.replace("{% static 'images/", "{% static 'book/images/")
    text = text.replace("{% static 'lay/", "{% static 'book/lay/")
    return text

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
    sftp = ssh.open_sftp()
    print("SSH/SFTP connected")

    temp_dir = os.path.join(PROJECT, '_book_temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # ============ Step 1: Download source files ============
    print("\n=== Step 1: Downloading source files ===")
    code_files = []
    for app in ['index', 'commodity', 'shopper']:
        for fn in ['models.py', 'views.py', 'urls.py', 'admin.py', '__init__.py']:
            code_files.append((f'{SRC}/{app}/{fn}', f'{temp_dir}/{app}/{fn}'))

    for fn in ['base.html', 'index.html', 'commodity.html', 'details.html',
               'shopcart.html', 'shopper.html', 'login.html']:
        code_files.append((f'{SRC}/templates/{fn}', f'{temp_dir}/templates/{fn}'))

    for remote, local in code_files:
        try:
            sftp_download(sftp, remote, local)
            print(f"  OK: {os.path.basename(os.path.dirname(remote))}/{os.path.basename(remote)}")
        except Exception as e:
            print(f"  SKIP: {os.path.basename(remote)} ({e})")

    sftp.close()
    ssh.close()
    print("  Disconnected from server (files downloaded)")

    # ============ Step 2: Fix encoding and rename apps ============
    print("\n=== Step 2: Fixing encoding and renaming apps ===")
    for old_name, new_name in APP_MAP.items():
        old_dir = os.path.join(temp_dir, old_name)
        new_dir = os.path.join(temp_dir, new_name)
        if not os.path.exists(old_dir):
            print(f"  SKIP: {old_name} not found")
            continue
        os.makedirs(new_dir, exist_ok=True)

        for fn in os.listdir(old_dir):
            old_path = os.path.join(old_dir, fn)
            new_path = os.path.join(new_dir, fn)
            if os.path.isfile(old_path) and fn.endswith('.py'):
                with open(old_path, 'rb') as f:
                    raw = f.read()
                text = fix_gbk(raw)
                text = fix_code_references(text)
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"  FIXED: {new_name}/{fn}")
            else:
                shutil.copy2(old_path, new_path)

    # ============ Step 3: Create apps.py ============
    print("\n=== Step 3: Creating apps.py files ===")
    apps_config = {
        'book_index': 'BookIndexConfig',
        'book_commodity': 'BookCommodityConfig',
        'book_shopper': 'BookShopperConfig',
    }
    for app_name, cls_name in apps_config.items():
        with open(os.path.join(temp_dir, app_name, 'apps.py'), 'w', encoding='utf-8') as f:
            f.write(f"from django.apps import AppConfig\n\nclass {cls_name}(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{app_name}'\n")
        print(f"  Created: {app_name}/apps.py")

    # ============ Step 4: Create migrations ============
    print("\n=== Step 4: Creating migrations directories ===")
    for app_name in APP_MAP.values():
        mig = os.path.join(temp_dir, app_name, 'migrations')
        os.makedirs(mig, exist_ok=True)
        with open(os.path.join(mig, '__init__.py'), 'w') as f:
            pass

    # ============ Step 5: Fix templates ============
    print("\n=== Step 5: Fixing template files ===")
    book_tpl = os.path.join(PROJECT, 'templates', 'book')
    if os.path.exists(book_tpl):
        shutil.rmtree(book_tpl)
    os.makedirs(book_tpl, exist_ok=True)

    tpl_dir = os.path.join(temp_dir, 'templates')
    for fn in os.listdir(tpl_dir):
        if fn.endswith('.html'):
            with open(os.path.join(tpl_dir, fn), 'rb') as f:
                raw = f.read()
            text = fix_gbk(raw)
            text = fix_template_references(text)
            with open(os.path.join(book_tpl, fn), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  Fixed: book/{fn}")

    # ============ Step 6: Copy apps to project ============
    print("\n=== Step 6: Copying apps to project directory ===")
    for app_name in APP_MAP.values():
        src_app = os.path.join(temp_dir, app_name)
        dst_app = os.path.join(PROJECT, app_name)
        if os.path.exists(dst_app):
            shutil.rmtree(dst_app)
        shutil.copytree(src_app, dst_app)
        print(f"  Copied: {app_name}/")

    # ============ Step 7: Update settings.py ============
    print("\n=== Step 7: Updating settings.py ===")
    settings_path = os.path.join(PROJECT, 'yigeworks', 'settings.py')
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = f.read()

    if "'book_commodity'" not in settings:
        settings = settings.replace(
            "'shop.apps.ShopConfig',",
            "'shop.apps.ShopConfig',\n    # Django3 Web开发教程示例应用\n    'book_index.apps.BookIndexConfig',\n    'book_commodity.apps.BookCommodityConfig',\n    'book_shopper.apps.BookShopperConfig',"
        )
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(settings)
    print("  Added 3 book apps to INSTALLED_APPS")

    # ============ Step 8: Update urls.py ============
    print("\n=== Step 8: Updating urls.py ===")
    urls_path = os.path.join(PROJECT, 'yigeworks', 'urls.py')
    with open(urls_path, 'r', encoding='utf-8') as f:
        urls = f.read()

    if "path('book/" not in urls:
        urls = urls.replace(
            "    # 用户账户",
            "    # Django3 Web开发教程示例应用\n    path('book/', include('book_index.urls')),\n    path('book/commodity/', include('book_commodity.urls')),\n    path('book/shopper/', include('book_shopper.urls')),\n\n    # 用户账户"
        )
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls)
    print("  Added book routes")

    # ============ Step 9: Update STATICFILES_DIRS ============
    print("\n=== Step 9: Updating STATICFILES_DIRS ===")
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = f.read()
    if "'book']" not in settings:
        settings = settings.replace(
            "STATICFILES_DIRS = [BASE_DIR / 'static']",
            "STATICFILES_DIRS = [BASE_DIR / 'static', BASE_DIR / 'static' / 'book']"
        )
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(settings)
        print("  Added book static dir")
    else:
        print("  Already has book static dir")

    # Cleanup temp
    shutil.rmtree(temp_dir)

    print("\n" + "=" * 60)
    print("LOCAL INTEGRATION COMPLETE!")
    print("=" * 60)
    print(f"\nNew apps created:")
    print(f"  - {PROJECT}/book_index/")
    print(f"  - {PROJECT}/book_commodity/")
    print(f"  - {PROJECT}/book_shopper/")
    print(f"\nTemplates created:")
    print(f"  - {PROJECT}/templates/book/")
    print(f"\nSettings updated:")
    print(f"  - INSTALLED_APPS: +3 book apps")
    print(f"  - urls.py: +3 book routes (/book/, /book/commodity/, /book/shopper/)")
    print(f"  - STATICFILES_DIRS: +static/book")

    print("\nNext: Run deploy_book.py to deploy to server")

if __name__ == '__main__':
    main()
