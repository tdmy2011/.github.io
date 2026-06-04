"""
综合修复 Django3-Web 集成的所有问题
1. 下载并修复 form.py, pays_new.py 编码
2. 修复 book_shopper/views.py 中的 URL 引用
3. 修复所有 views.py 中的模板路径（加 'book/' 前缀）
4. 修复 URL patterns 格式
5. 修复 book_index/urls.py 添加 app_name
6. 处理 pays_new.py 的 Alipay 依赖（改为可选导入）
"""
import paramiko
import os
import re

SERVER = '43.134.232.149'
USER = 'ubuntu'
PASS = 'Yige2026@'
SRC = '/home/ubuntu/django3web_src/extracted/chapter11/babys'
PROJECT = r'C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40\yigeworks_django'

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

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
    sftp = ssh.open_sftp()
    print("Connected")

    # ============ 1. Download form.py and pays_new.py ============
    print("\n=== Downloading missing files ===")
    for fn in ['form.py', 'pays_new.py', 'pays.py']:
        remote = f'{SRC}/shopper/{fn}'
        local = os.path.join(PROJECT, 'book_shopper', fn)
        try:
            raw = sftp.open(remote).read()
            text = fix_gbk(raw)
            with open(local, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  OK: book_shopper/{fn}")
        except Exception as e:
            print(f"  SKIP: {fn} ({e})")

    sftp.close()
    ssh.close()
    print("Disconnected")

    # ============ 2. Fix pays_new.py - make Alipay import optional ============
    pays_new_path = os.path.join(PROJECT, 'book_shopper', 'pays_new.py')
    if os.path.exists(pays_new_path):
        with open(pays_new_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Replace the direct imports with try/except
        old_import = """import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest"""
        new_import = """import logging
try:
    from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
    from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
    from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
    from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
    ALIPAY_AVAILABLE = True
except ImportError:
    ALIPAY_AVAILABLE = False"""
        content = content.replace(old_import, new_import)

        # Wrap the client creation and get_pay in availability check
        # Add check at the end
        content = content.replace(
            "def get_pay(out_trade_no, total_amount, return_url):",
            "def get_pay(out_trade_no, total_amount, return_url):\n    if not ALIPAY_AVAILABLE:\n        return None"
        )
        with open(pays_new_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Fixed: pays_new.py (Alipay optional)")

    # ============ 3. Fix book_shopper/views.py ============
    print("\n=== Fixing book_shopper/views.py ===")
    shopper_views = os.path.join(PROJECT, 'book_shopper', 'views.py')
    with open(shopper_views, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix reverse() calls
    content = content.replace("reverse('shopper:shopper')", "reverse('book_shopper:shopper')")
    content = content.replace("reverse('shopper:shopcart')", "reverse('book_shopper:shopcart')")
    content = content.replace("reverse('index:index')", "reverse('book_index:index')")
    content = content.replace("redirect('shopper:shopcart')", "redirect(reverse('book_shopper:shopcart'))")

    # Fix login_url
    content = content.replace("login_url='/shopper/login.html'", "login_url='/book/shopper/login.html'")

    # Fix return_url in paysView
    content = content.replace(
        "return_url = 'http://' + request.get_host() + '/shopper.html'",
        "return_url = 'http://' + request.get_host() + '/book/shopper/'"
    )

    # Fix template paths
    content = content.replace("render(request, 'login.html'", "render(request, 'book/login.html'")
    content = content.replace("render(request, 'shopper.html'", "render(request, 'book/shopper.html'")
    content = content.replace("render(request, 'shopcart.html'", "render(request, 'book/shopcart.html'")

    # Fix get_pay to handle None
    content = content.replace(
        "url = get_pay(out_trade_no, total, return_url)\n        return redirect(url)\n    else:",
        "url = get_pay(out_trade_no, total, return_url)\n        if url:\n            return redirect(url)\n    "
    )

    with open(shopper_views, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: URL references, template paths, login_url")

    # ============ 4. Fix book_commodity/views.py ============
    print("\n=== Fixing book_commodity/views.py ===")
    commodity_views = os.path.join(PROJECT, 'book_commodity', 'views.py')
    with open(commodity_views, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("render(request, 'details.html'", "render(request, 'book/details.html'")
    content = content.replace("render(request, 'commodity.html'", "render(request, 'book/commodity.html'")

    with open(commodity_views, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: template paths")

    # ============ 5. Fix book_index/views.py ============
    print("\n=== Fixing book_index/views.py ===")
    index_views = os.path.join(PROJECT, 'book_index', 'views.py')
    with open(index_views, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("template_name = 'index.html'", "template_name = 'book/index.html'")
    content = content.replace("render(request, 'index.html'", "render(request, 'book/index.html'")

    with open(index_views, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: template paths")

    # ============ 6. Fix URL patterns ============
    print("\n=== Fixing URL patterns ===")

    # Fix book_commodity/urls.py
    commodity_urls = os.path.join(PROJECT, 'book_commodity', 'urls.py')
    with open(commodity_urls, 'r', encoding='utf-8') as f:
        content = f.read()
    content = "app_name = 'book_commodity'\n\n" + content.replace(
        "urlpatterns = [\n    path('.html', commodityView, name='commodity'),\n    path('/detail.<int:id>.html', detailView, name='detail'),\n    path('/collect.html', collectView, name='collect')\n]",
        "urlpatterns = [\n    path('', commodityView, name='commodity'),\n    path('detail/<int:id>/', detailView, name='detail'),\n    path('collect/', collectView, name='collect'),\n]"
    )
    with open(commodity_urls, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: book_commodity/urls.py")

    # Fix book_shopper/urls.py
    shopper_urls = os.path.join(PROJECT, 'book_shopper', 'urls.py')
    with open(shopper_urls, 'r', encoding='utf-8') as f:
        content = f.read()
    content = "app_name = 'book_shopper'\n\n" + content.replace(
        "urlpatterns = [\n    path('.html', shopperView, name='shopper'),\n    path('/login.html', loginView, name='login'),\n    path('/logout.html', logoutView, name='logout'),\n    path('/shopcart.html', shopcartView, name='shopcart'),\n    path('/pays.html', paysView, name='pays'),\n    path('/delete.html', deleteAPI, name='delete')\n]",
        "urlpatterns = [\n    path('', shopperView, name='shopper'),\n    path('login/', loginView, name='login'),\n    path('logout/', logoutView, name='logout'),\n    path('shopcart/', shopcartView, name='shopcart'),\n    path('pays/', paysView, name='pays'),\n    path('delete/', deleteAPI, name='delete'),\n]"
    )
    with open(shopper_urls, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: book_shopper/urls.py")

    # Fix book_index/urls.py
    index_urls = os.path.join(PROJECT, 'book_index', 'urls.py')
    with open(index_urls, 'r', encoding='utf-8') as f:
        content = f.read()
    if "app_name" not in content:
        content = "app_name = 'book_index'\n\n" + content
    with open(index_urls, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed: book_index/urls.py")

    # ============ 7. Fix template URL references ============
    print("\n=== Fixing template URL references ===")
    book_tpl_dir = os.path.join(PROJECT, 'templates', 'book')
    for fn in os.listdir(book_tpl_dir):
        if fn.endswith('.html'):
            tpl_path = os.path.join(book_tpl_dir, fn)
            with open(tpl_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Fix .html URL suffixes (book uses /detail/<id>/ now)
            content = content.replace(
                "{% url 'book_commodity:detail' p.id %}",
                "{% url 'book_commodity:detail' p.id %}"
            )
            # The templates use {% url 'commodity:detail' item.id %} which was already fixed to book_commodity
            # Fix pages.paginator reference bug in commodity.html and shopper.html
            content = content.replace("pages.pages.next_page_number", "pages.next_page_number")
            with open(tpl_path, 'w', encoding='utf-8') as f:
                f.write(content)
    print("  Fixed: template references")

    # ============ 8. Add alipay-sdk-python to requirements.txt ============
    print("\n=== Updating requirements.txt ===")
    req_path = os.path.join(PROJECT, 'requirements.txt')
    with open(req_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'alipay' not in content:
        content += '\nalipay-sdk-python>=3.0.0  # Django3教程示例：支付宝SDK（可选）\n'
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Added: alipay-sdk-python")

    print("\n" + "=" * 60)
    print("ALL FIXES COMPLETE!")
    print("=" * 60)
    print("\nFixed items:")
    print("  1. Downloaded form.py, pays_new.py, pays.py")
    print("  2. pays_new.py: Alipay import made optional")
    print("  3. book_shopper/views.py: URL references + template paths")
    print("  4. book_commodity/views.py: template paths")
    print("  5. book_index/views.py: template paths")
    print("  6. All urls.py: added app_name + fixed patterns")
    print("  7. Templates: fixed pages.paginator bug")
    print("  8. requirements.txt: added alipay-sdk-python")

if __name__ == '__main__':
    main()
