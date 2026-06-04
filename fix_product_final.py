"""Fix product detail template properly."""
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

# Rewrite product_detail.html with proper if/endif
template = '''{% extends "base.html" %}
{% load static %}

{% block title %}{{ product.name }} - YiGe Works{% endblock %}

{% block content %}
<section style="max-width: 1200px; margin: 0 auto; padding: 60px 24px;">

  {# 左右两栏布局 #}
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 48px; margin-bottom: 60px;">

    {# 左侧：商品图片 #}
    <div>
      <div style="border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; background: #f8fafc;">
        {% if product.image %}
        <img src="{{ product.image.url }}" alt="{{ product.name }}" style="width: 100%; height: auto; display: block; object-fit: cover;">
        {% else %}
        <div style="width: 100%; height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 1.2rem;">暂无图片</div>
        {% endif %}
      </div>
    </div>

    {# 右侧：商品信息 #}
    <div>
      <h1 style="font-size: 2rem; font-weight: 700; color: #0f172a; margin-bottom: 12px;">{{ product.name }}</h1>

      <p style="font-size: 1rem; color: #64748b; line-height: 1.7; margin-bottom: 24px;">{{ product.description }}</p>

      {# 价格 #}
      <div style="margin-bottom: 24px;">
        {% if product.has_discount %}
        <span style="font-size: 2rem; font-weight: 700; color: #dc2626;">${{ product.effective_price_usd }}</span>
        <span style="font-size: 1.25rem; color: #94a3b8; text-decoration: line-through; margin-left: 12px;">${{ product.price_usd }}</span>
        {% else %}
        <span style="font-size: 2rem; font-weight: 700; color: #1e40af;">${{ product.price_usd }}</span>
        {% endif %}
      </div>

      {# 特点列表 #}
      {% if product.feature_list_zh %}
      <div style="margin-bottom: 28px;">
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1e293b; margin-bottom: 12px;">产品特点</h3>
        <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
          {% for feature in product.feature_list_zh %}
          <li style="display: flex; align-items: flex-start; gap: 10px; font-size: 0.95rem; color: #475569;">
            <span style="color: #3b82f6; font-weight: 700; flex-shrink: 0;">&#10003;</span>
            <span>{{ feature }}</span>
          </li>
          {% endfor %}
        </ul>
      </div>
      {% endif %}

      {# 加入购物车按钮 #}
      <form method="post" action="{% url 'shop:cart_add' product.id %}" style="margin-bottom: 16px;">
        {% csrf_token %}
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
          <label for="quantity" style="font-size: 0.95rem; color: #475569;">数量</label>
          <input type="number" id="quantity" name="quantity" value="1" min="1" style="width: 64px; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; text-align: center; font-size: 0.95rem;">
        </div>
        <button type="submit" style="display: block; width: 100%; padding: 14px; border: none; border-radius: 8px; background: linear-gradient(135deg, #1e40af, #3b82f6); color: #fff; cursor: pointer; font-size: 1.05rem; font-weight: 600;">加入购物车</button>
      </form>

      <p style="font-size: 0.85rem; color: #94a3b8;">
        {% if product.stock > 0 %}
        库存充足，付款后即时处理
        {% else %}
        暂时缺货
        {% endif %}
      </p>
    </div>
  </div>

  {# 相关商品 #}
  {% if related %}
  <div>
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 24px;">相关商品</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 24px;">
      {% for rel_product in related %}
      <a href="{% url 'products:detail' rel_product.slug %}" style="text-decoration: none;">
        <div class="product-card" style="overflow: hidden;">
          <div style="border-radius: 8px; overflow: hidden; margin-bottom: 12px; background: #f1f5f9;">
            {% if rel_product.image %}
            <img src="{{ rel_product.image.url }}" alt="{{ rel_product.name }}" style="width: 100%; height: 180px; object-fit: cover; display: block;">
            {% else %}
            <div style="width: 100%; height: 180px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">暂无图片</div>
            {% endif %}
          </div>
          <h3 style="font-size: 1rem; font-weight: 600; color: #0f172a; margin-bottom: 6px;">{{ rel_product.name }}</h3>
          <span style="font-weight: 700; color: #1e40af;">${{ rel_product.price_usd }}</span>
        </div>
      </a>
      {% endfor %}
    </div>
  </div>
  {% endif %}

</section>
{% endblock %}
'''

with sftp.open(f'{RDIR}/templates/products/product_detail.html', 'w') as f:
    f.write(template)
print('  Rewrote product_detail.html with proper if/endif blocks')

# Also fix blog post_detail.html - make sure if/endif is complete
blog_template = run(f'cat {RDIR}/templates/blog/post_detail.html')
# Check if it has endif
if '{% endif %}' not in blog_template:
    # Add endif for cover_image
    blog_template = blog_template.replace(
        '{% if post.cover_image %}<img src="{{ post.cover_image.url }}"',
        '{% if post.cover_image %}<img src="{{ post.cover_image.url }}"\n            {% endif %}'
    )
    with sftp.open(f'{RDIR}/templates/blog/post_detail.html', 'w') as f:
        f.write(blog_template)
    print('  Fixed blog post_detail.html endif')

# Restore DEBUG=False
settings = run(f'cat {RDIR}/yigeworks/settings.py')
lines = settings.split('\n')
restore = []
for line in lines:
    if 'DEBUG = True' in line.strip() and '# TEMP' not in line:
        restore.append('DEBUG = False')
    else:
        restore.append(line)
with sftp.open(f'{RDIR}/yigeworks/settings.py', 'w') as f:
    f.write('\n'.join(restore))
run('sudo systemctl restart yigeworks 2>&1')

import time; time.sleep(3)

# Verify all pages
print('\n=== Final verification ===')
pages = [
    ('/', 'Home'),
    ('/products/', 'Products'),
    ('/products/detail/iso45001-lead-auditor/', 'Product 1'),
    ('/products/detail/iso14001-lead-auditor/', 'Product 2'),
    ('/products/detail/safety-manual-template/', 'Product 3'),
    ('/products/detail/dual-system-consulting/', 'Product 4'),
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
    print('\n  >>> ALL 20 PAGES OK! <<<')

# External test
print('\n=== External test ===')
out = run(f'curl -s -o /dev/null -w "%{{http_code}}" http://43.134.232.149/')
print(f'  External: {out.strip()}')

sftp.close()
ssh.close()
print('\nDone!')
