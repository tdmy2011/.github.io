"""
批量生成所有前端模板文件
每个模板 extends base.html，继承完整的导航栏和页脚
"""
import os

BASE = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_shop'

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK: {path}')

# ========== 1. Home Page ==========
write('shop/templates/shop/home.html', '''{% extends "base.html" %}
{% load static %}

{% block title %}YigeWorks - ISO 45001+ISO 14001双体系落地{% endblock %}

{% block content %}
<!-- Hero -->
<section class="hero">
    <div class="container">
        <div class="hero-inner">
            <div>
                <h1>30天ISO 45001+ISO 14001<br>双体系落地营</h1>
                <p>30年安全环保实战专家，帮助在东南亚/非洲建厂的中资企业，快速通过国际认证，零事故投产运营。</p>
                <div style="display:flex;gap:16px;flex-wrap:wrap;">
                    <a href="{% url 'shop:product_list' %}" class="btn btn-accent btn-lg">立即选购课程</a>
                    <a href="{% url 'shop:pricing' %}" class="btn btn-outline btn-lg" style="color:#fff;border-color:#fff;">查看定价方案</a>
                </div>
                <div class="trust-badges">
                    <div class="trust-badge">✓ ISO 45001认证</div>
                    <div class="trust-badge">✓ ISO 14001认证</div>
                    <div class="trust-badge">✓ 30年实战经验</div>
                    <div class="trust-badge">✓ 500+企业服务</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Categories -->
<section class="section">
    <div class="container">
        <h2 class="section-title">课程分类</h2>
        <p class="section-subtitle">选择适合您的专业课程</p>
        <div class="card-grid">
            {% for cat in categories %}
            <a href="{% url 'shop:product_list_by_category' cat.slug %}" class="card" style="text-decoration:none;">
                <div style="font-size:2.5rem;margin-bottom:12px;">📚</div>
                <h3>{{ cat.name }}</h3>
                <p style="color:var(--gray-500);font-size:0.9rem;margin-top:8px;">
                    {{ cat.products.count }} 个课程
                </p>
            </a>
            {% empty %}
            <div class="card" style="text-align:center;padding:40px;">
                <p style="color:var(--gray-500);">分类加载中...</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Featured Products -->
<section class="section" style="background:var(--gray-50);">
    <div class="container">
        <h2 class="section-title">热门课程</h2>
        <p class="section-subtitle">精选最受欢迎的课程产品</p>
        <div class="card-grid">
            {% for product in all_products %}
            <div class="card product-card">
                <div class="card-image">
                    {% if product.product_type == 'course' %}🎓{% elif product.product_type == 'template' %}📄{% elif product.product_type == 'service' %}🤝{% else %}📋{% endif %}
                </div>
                <div class="card-body">
                    <span class="tag tag-blue">{{ product.get_product_type_display }}</span>
                    <h3 style="margin-top:8px;">{{ product.name }}</h3>
                    <p>{{ product.short_description|truncatechars:80 }}</p>
                    <div class="price-row">
                        <span class="price">${{ product.price }}</span>
                        {% if product.original_price > product.price %}
                        <span class="original-price">${{ product.original_price }}</span>
                        <span class="discount">-{{ product.discount_percent }}%</span>
                        {% endif %}
                    </div>
                    <a href="{% url 'shop:product_detail' product.slug %}" class="btn btn-primary btn-sm" style="margin-top:12px;width:100%;">查看详情</a>
                </div>
            </div>
            {% empty %}
            <div class="card" style="text-align:center;padding:60px;grid-column:1/-1;">
                <h3>课程上线中</h3>
                <p style="color:var(--gray-500);margin-top:8px;">我们正在准备精彩课程，敬请期待！</p>
                <a href="{% url 'shop:contact' %}" class="btn btn-outline mt-4">联系我们</a>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- FAQ -->
{% if faqs %}
<section class="section">
    <div class="container">
        <h2 class="section-title">常见问题</h2>
        <p class="section-subtitle">关于课程和服务的常见疑问</p>
        <div style="max-width:800px;margin:0 auto;">
            {% for faq in faqs %}
            <div class="faq-item">
                <div class="faq-question">{{ faq.question_zh }}</div>
                <div class="faq-answer">{{ faq.answer_zh }}</div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}

<!-- CTA -->
<section class="section" style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;text-align:center;">
    <div class="container">
        <h2 style="color:#fff;margin-bottom:16px;">准备好提升企业安全合规水平了吗？</h2>
        <p style="opacity:0.9;margin-bottom:32px;font-size:1.1rem;">立即加入30天双体系落地营，让专业的人做专业的事</p>
        <a href="{% url 'shop:product_list' %}" class="btn btn-accent btn-lg">立即选购</a>
    </div>
</section>

<!-- Newsletter -->
<section class="section">
    <div class="container" style="text-align:center;">
        <h2 class="section-title">订阅获取最新资讯</h2>
        <p class="section-subtitle">第一时间获取新课程上线和安全合规资讯</p>
        <form id="newsletterForm" style="max-width:480px;margin:0 auto;display:flex;gap:12px;">
            <input type="email" name="email" class="form-input" placeholder="输入您的邮箱" required style="flex:1;">
            <button type="submit" class="btn btn-primary">订阅</button>
        </form>
    </div>
</section>

<script>
document.getElementById('newsletterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var fd = new FormData(this);
    fetch('{% url "shop:newsletter_signup" %}', {method:'POST', body:fd, headers:{'X-Requested-With':'XMLHttpRequest'}})
    .then(r => r.json()).then(d => showToast(d.message || d.status));
});
</script>
{% endblock %}
''')

# ========== 2. Product List ==========
write('shop/templates/shop/product_list.html', '''{% extends "base.html" %}

{% block title %}课程产品{% if category %} - {{ category.name }}{% endif %} | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 class="section-title">{% if category %}{{ category.name }}{% else %}全部课程产品{% endif %}</h1>

        <!-- Category Filter -->
        <div style="display:flex;gap:8px;margin-bottom:40px;flex-wrap:wrap;justify-content:center;">
            <a href="{% url 'shop:product_list' %}" class="btn btn-sm {% if not category %}btn-primary{% else %}btn-outline{% endif %}">全部</a>
            {% for cat in categories %}
            <a href="{% url 'shop:product_list_by_category' cat.slug %}" class="btn btn-sm {% if category and category.slug == cat.slug %}btn-primary{% else %}btn-outline{% endif %}">{{ cat.name }}</a>
            {% endfor %}
        </div>

        <!-- Products Grid -->
        <div class="card-grid">
            {% for product in products %}
            <div class="card product-card">
                <div class="card-image">
                    {% if product.product_type == 'course' %}🎓{% elif product.product_type == 'template' %}📄{% elif product.product_type == 'service' %}🤝{% else %}📋{% endif %}
                </div>
                <div class="card-body">
                    <span class="tag tag-blue">{{ product.get_product_type_display }}</span>
                    <h3 style="margin-top:8px;"><a href="{% url 'shop:product_detail' product.slug %}">{{ product.name }}</a></h3>
                    <p>{{ product.short_description|truncatechars:80 }}</p>
                    {% if product.duration %}<p style="font-size:0.85rem;color:var(--gray-400);">⏱ {{ product.duration }} | 📚 {{ product.modules }} 课时</p>{% endif %}
                    <div class="price-row">
                        <span class="price">${{ product.price }}</span>
                        {% if product.original_price > product.price %}
                        <span class="original-price">${{ product.original_price }}</span>
                        <span class="discount">-{{ product.discount_percent }}%</span>
                        {% endif %}
                    </div>
                    <div style="display:flex;gap:8px;margin-top:12px;">
                        <a href="{% url 'shop:product_detail' product.slug %}" class="btn btn-primary btn-sm" style="flex:1;">查看详情</a>
                        <form method="post" action="{% url 'shop:cart_add' product.id %}" style="flex:1;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-accent btn-sm" style="width:100%;">加入购物车</button>
                        </form>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="card" style="text-align:center;padding:60px;grid-column:1/-1;">
                <h3>暂无课程</h3>
                <p style="color:var(--gray-500);margin-top:8px;">课程正在准备中，请稍后再来</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 3. Product Detail ==========
write('shop/templates/shop/product_detail.html', '''{% extends "base.html" %}

{% block title %}{{ product.name }} | YigeWorks{% endblock %}
{% block og_title %}{{ product.name }}{% endblock %}
{% block og_desc %}{{ product.short_description }}{% endblock %}
{% block canonical %}/product/{{ product.slug }}/{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <!-- Breadcrumb -->
        <div style="margin-bottom:24px;font-size:0.85rem;color:var(--gray-500);">
            <a href="{% url 'shop:home' %}">首页</a> &rsaquo;
            <a href="{% url 'shop:product_list' %}">课程产品</a> &rsaquo;
            {% if product.category %}<a href="{{ product.category.get_absolute_url }}">{{ product.category.name }}</a> &rsaquo;{% endif %}
            {{ product.name }}
        </div>

        <!-- Product Info -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">
            <!-- Left: Image -->
            <div class="card" style="aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;font-size:5rem;background:linear-gradient(135deg,var(--primary-light),var(--gray-100));">
                {% if product.product_type == 'course' %}🎓{% elif product.product_type == 'template' %}📄{% elif product.product_type == 'service' %}🤝{% else %}📋{% endif %}
            </div>

            <!-- Right: Details -->
            <div>
                <span class="tag tag-blue">{{ product.get_product_type_display }}</span>
                <h1 style="font-size:2rem;margin-top:12px;">{{ product.name }}</h1>
                <p style="color:var(--gray-500);margin-top:8px;">{{ product.short_description }}</p>

                <div style="margin-top:24px;padding:24px;background:var(--gray-50);border-radius:8px;">
                    <div class="price-row" style="margin-bottom:16px;">
                        <span style="font-size:2rem;font-weight:800;color:var(--primary);">${{ product.price }}</span>
                        {% if product.original_price > product.price %}
                        <span class="original-price" style="font-size:1.2rem;">${{ product.original_price }}</span>
                        <span class="discount">省 ${{ product.original_price|add:"0"|floatformat:2 }}</span>
                        {% endif %}
                    </div>
                    <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:0.9rem;color:var(--gray-500);">
                        {% if product.duration %}<span>⏱ {{ product.duration }}</span>{% endif %}
                        {% if product.modules %}<span>📚 {{ product.modules }} 课时</span>{% endif %}
                    </div>
                </div>

                <form method="post" action="{% url 'shop:cart_add' product.id %}" style="display:flex;gap:12px;margin-top:24px;flex-wrap:wrap;">
                    {% csrf_token %}
                    <div style="display:flex;align-items:center;border:1px solid var(--gray-300);border-radius:8px;overflow:hidden;">
                        <button type="button" onclick="changeQty(-1)" class="btn btn-sm" style="border:none;border-radius:0;">−</button>
                        <input type="number" name="quantity" value="1" min="1" max="99" id="qty" style="width:60px;text-align:center;border:none;font-size:1rem;padding:8px;">
                        <button type="button" onclick="changeQty(1)" class="btn btn-sm" style="border:none;border-radius:0;">+</button>
                    </div>
                    <button type="submit" class="btn btn-accent btn-lg" style="flex:1;">🛒 加入购物车</button>
                </form>

                <p style="margin-top:16px;font-size:0.85rem;color:var(--gray-400);">✓ 即时购买 ✓ 安全支付（PayPal） ✓ 购买后永久访问</p>
            </div>
        </div>

        <!-- Description -->
        <div class="card mt-8">
            <h2 style="margin-bottom:16px;">课程详情</h2>
            <div style="line-height:1.8;color:var(--gray-600);">{{ product.description|linebreaks }}</div>
        </div>

        <!-- Curriculum (for courses) -->
        {% if modules %}
        <div class="card mt-8">
            <h2 style="margin-bottom:24px;">📚 课程大纲</h2>
            {% for module in modules %}
            <div style="border:1px solid var(--gray-200);border-radius:8px;margin-bottom:12px;overflow:hidden;">
                <div style="padding:16px 20px;background:var(--gray-50);font-weight:600;display:flex;justify-content:space-between;align-items:center;">
                    <span>模块 {{ module.order }}：{{ module.title }}</span>
                    <span style="font-size:0.85rem;color:var(--gray-400);">{{ module.duration }}</span>
                </div>
                {% if module.description %}
                <div style="padding:12px 20px;color:var(--gray-500);font-size:0.9rem;">{{ module.description }}</div>
                {% endif %}
                {% if module.deliverables %}
                <div style="padding:8px 20px;font-size:0.85rem;color:var(--green);">📦 交付物：{{ module.deliverables }}</div>
                {% endif %}
                {% for lesson in module.lessons.all %}
                <div style="padding:12px 20px 12px 40px;border-top:1px solid var(--gray-100);display:flex;justify-content:space-between;align-items:center;font-size:0.9rem;">
                    <span>{{ lesson.order }}. {{ lesson.title }}</span>
                    <span style="color:var(--gray-400);font-size:0.8rem;">{{ lesson.duration }} {% if lesson.is_free %}<span class="tag tag-green">免费试看</span>{% endif %}</span>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- Related Products -->
        {% if related %}
        <div class="mt-8">
            <h2 class="section-title" style="font-size:1.5rem;">相关课程</h2>
            <div class="card-grid" style="margin-top:24px;">
                {% for p in related %}
                <div class="card product-card">
                    <div class="card-image">{% if p.product_type == 'course' %}🎓{% else %}📄{% endif %}</div>
                    <div class="card-body">
                        <h3><a href="{% url 'shop:product_detail' p.slug %}">{{ p.name }}</a></h3>
                        <div class="price-row"><span class="price">${{ p.price }}</span></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</section>

<script>
function changeQty(d) {
    var el = document.getElementById('qty');
    var v = parseInt(el.value) + d;
    if (v < 1) v = 1;
    if (v > 99) v = 99;
    el.value = v;
}
</script>
{% endblock %}
''')

# ========== 4. Cart Detail ==========
write('shop/templates/shop/cart_detail.html', '''{% extends "base.html" %}

{% block title %}购物车 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 class="section-title">🛒 购物车</h1>

        {% if cart|length > 0 %}
        <div style="display:grid;grid-template-columns:2fr 1fr;gap:32px;align-items:start;">
            <!-- Cart Items -->
            <div>
                {% for item in cart %}
                <div class="card" style="display:flex;gap:20px;align-items:center;margin-bottom:16px;">
                    <div style="width:80px;height:80px;border-radius:8px;background:var(--primary-light);display:flex;align-items:center;justify-content:center;font-size:2rem;flex-shrink:0;">
                        📦
                    </div>
                    <div style="flex:1;">
                        <h3><a href="{% url 'shop:product_detail' item.product.slug %}">{{ item.name }}</a></h3>
                        <div style="display:flex;gap:16px;align-items:center;margin-top:8px;">
                            <div style="display:flex;align-items:center;border:1px solid var(--gray-300);border-radius:6px;overflow:hidden;">
                                <button onclick="updateCart({{ item.product.id }}, {{ item.quantity }}-1)" class="btn btn-sm" style="border:none;border-radius:0;padding:4px 10px;">−</button>
                                <input type="number" value="{{ item.quantity }}" min="0" id="qty_{{ item.product.id }}" style="width:48px;text-align:center;border:none;font-size:0.9rem;padding:4px;" readonly>
                                <button onclick="updateCart({{ item.product.id }}, {{ item.quantity }}+1)" class="btn btn-sm" style="border:none;border-radius:0;padding:4px 10px;">+</button>
                            </div>
                            <span style="font-weight:700;color:var(--primary);">${{ item.total_price }}</span>
                        </div>
                    </div>
                    <button onclick="removeFromCart({{ item.product.id }})" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:var(--gray-400);padding:8px;" title="删除">✕</button>
                </div>
                {% endfor %}
                <a href="{% url 'shop:cart_clear' %}" class="btn btn-sm" style="color:var(--red);">清空购物车</a>
            </div>

            <!-- Summary -->
            <div class="card" style="position:sticky;top:80px;">
                <h3 style="margin-bottom:16px;">订单摘要</h3>
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                    <span>商品总数</span>
                    <span>{{ cart|length }} 件</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:var(--gray-400);">
                    <span>原价</span>
                    <span>${{ cart.get_total_original }}</span>
                </div>
                {% if cart.get_total_original > cart.get_total_price %}
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:var(--red);">
                    <span>优惠</span>
                    <span>-${{ cart.get_total_original|add:"0"|floatformat:2 }}</span>
                </div>
                {% endif %}
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:var(--gray-400);">
                    <span>运费</span>
                    <span>免费（数字产品）</span>
                </div>
                <div style="border-top:2px solid var(--gray-200);padding-top:16px;margin-top:16px;display:flex;justify-content:space-between;font-size:1.2rem;font-weight:700;">
                    <span>应付总额</span>
                    <span style="color:var(--primary);">${{ cart.get_total_price }}</span>
                </div>
                <a href="{% url 'orders:checkout' %}" class="btn btn-accent btn-lg mt-4" style="width:100%;">去结算</a>
                <a href="{% url 'shop:product_list' %}" class="btn btn-outline btn-sm mt-4" style="width:100%;">继续购物</a>
            </div>
        </div>

        {% else %}
        <div class="card" style="text-align:center;padding:80px;">
            <div style="font-size:4rem;margin-bottom:16px;">🛒</div>
            <h2>购物车是空的</h2>
            <p style="color:var(--gray-500);margin-top:8px;">去浏览我们的课程产品吧！</p>
            <a href="{% url 'shop:product_list' %}" class="btn btn-primary mt-4">浏览课程</a>
        </div>
        {% endif %}
    </div>
</section>

<script>
function updateCart(pid, newQty) {
    if (newQty < 1) { removeFromCart(pid); return; }
    fetch('{% url "shop:cart_update" pid %}', {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
        body: 'quantity=' + newQty
    }).then(r => r.json()).then(d => { if (d.status === 'ok') location.reload(); });
}
function removeFromCart(pid) {
    if (!confirm('确定要删除这个商品吗？')) return;
    fetch('{% url "shop:cart_remove" pid %}', {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
    }).then(r => r.json()).then(d => { if (d.status === 'ok') location.reload(); });
}
</script>
{% endblock %}
''')

# ========== 5. Checkout ==========
write('orders/templates/orders/checkout.html', '''{% extends "base.html" %}

{% block title %}结算 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 class="section-title">填写订单信息</h1>

        <div style="display:grid;grid-template-columns:2fr 1fr;gap:32px;align-items:start;max-width:1000px;margin:0 auto;">
            <!-- Form -->
            <form method="post" action="{% url 'orders:checkout' %}" class="card">
                {% csrf_token %}
                <h3 style="margin-bottom:20px;">联系信息</h3>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                    <div class="form-group">{{ form.first_name.label_tag }}{{ form.first_name }}</div>
                    <div class="form-group">{{ form.last_name.label_tag }}{{ form.last_name }}</div>
                </div>
                <div class="form-group">{{ form.email.label_tag }}{{ form.email }}</div>
                <div class="form-group">{{ form.company.label_tag }}{{ form.company }}</div>
                <div class="form-group">{{ form.phone.label_tag }}{{ form.phone }}</div>

                <h3 style="margin:24px 0 20px;">支付方式</h3>
                <div class="form-group">
                    <label style="display:flex;align-items:center;gap:12px;padding:16px;border:2px solid var(--primary);border-radius:8px;cursor:pointer;margin-bottom:8px;">
                        <input type="radio" name="payment_method" value="paypal" checked style="width:18px;height:18px;">
                        <span style="font-weight:600;">PayPal</span>
                        <span style="color:var(--gray-400);font-size:0.85rem;">推荐 · 国际信用卡/借记卡</span>
                    </label>
                    <label style="display:flex;align-items:center;gap:12px;padding:16px;border:1px solid var(--gray-200);border-radius:8px;cursor:pointer;margin-bottom:8px;">
                        <input type="radio" name="payment_method" value="stripe" style="width:18px;height:18px;">
                        <span style="font-weight:600;">Stripe</span>
                        <span style="color:var(--gray-400);font-size:0.85rem;">即将上线</span>
                    </label>
                    <label style="display:flex;align-items:center;gap:12px;padding:16px;border:1px solid var(--gray-200);border-radius:8px;cursor:pointer;">
                        <input type="radio" name="payment_method" value="transfer" style="width:18px;height:18px;">
                        <span style="font-weight:600;">银行转账</span>
                        <span style="color:var(--gray-400);font-size:0.85rem;">联系客服获取账号</span>
                    </label>
                </div>

                <button type="submit" class="btn btn-accent btn-lg" style="width:100%;margin-top:24px;">确认订单，去支付 ${{ cart.get_total_price }}</button>
                <p style="text-align:center;margin-top:12px;font-size:0.85rem;color:var(--gray-400);">
                    提交订单后将被引导至支付页面
                </p>
            </form>

            <!-- Order Summary -->
            <div class="card" style="position:sticky;top:80px;">
                <h3 style="margin-bottom:16px;">订单明细</h3>
                {% for item in cart %}
                <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--gray-100);font-size:0.9rem;">
                    <span>{{ item.name }} x{{ item.quantity }}</span>
                    <span style="font-weight:600;">${{ item.total_price }}</span>
                </div>
                {% endfor %}
                <div style="border-top:2px solid var(--gray-200);padding-top:16px;margin-top:8px;display:flex;justify-content:space-between;font-size:1.2rem;font-weight:700;">
                    <span>总计</span>
                    <span style="color:var(--primary);">${{ cart.get_total_price }}</span>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
document.querySelectorAll('input[name=payment_method]').forEach(r => {
    r.addEventListener('change', function() {
        document.querySelectorAll('label').forEach(l => l.style.borderColor = 'var(--gray-200)');
        this.closest('label').style.borderColor = 'var(--primary)';
    });
});
</script>
{% endblock %}
''')

# ========== 6. Payment Process ==========
write('payment/templates/payment/process.html', '''{% extends "base.html" %}

{% block title %}支付 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:640px;">
        <h1 class="section-title">确认支付</h1>

        <div class="card">
            <!-- Order Info -->
            <div style="background:var(--gray-50);border-radius:8px;padding:20px;margin-bottom:24px;">
                <h3 style="margin-bottom:12px;">订单 #{{ order.id }}</h3>
                {% for item in order.items.all %}
                <div style="display:flex;justify-content:space-between;padding:6px 0;font-size:0.9rem;">
                    <span>{{ item.product_name }} x{{ item.quantity }}</span>
                    <span>${{ item.total }}</span>
                </div>
                {% endfor %}
                <div style="border-top:2px solid var(--gray-200);padding-top:12px;margin-top:8px;display:flex;justify-content:space-between;font-size:1.3rem;font-weight:700;">
                    <span>应付总额</span>
                    <span style="color:var(--primary);">${{ order.total_paid }} {{ order.currency }}</span>
                </div>
            </div>

            <!-- PayPal Button -->
            {% if payment_method == 'paypal' %}
            <div id="paypal-button-container" style="min-height:50px;text-align:center;"></div>
            <p style="text-align:center;margin-top:16px;font-size:0.85rem;color:var(--gray-400);">
                点击上方按钮将跳转到 PayPal 完成支付
            </p>
            {% elif payment_method == 'stripe' %}
            <div style="text-align:center;padding:40px;">
                <p style="color:var(--gray-500);">Stripe 支付即将上线</p>
                <p style="font-size:0.85rem;color:var(--gray-400);margin-top:8px;">请联系客服完成支付：admin@yigeworks.com</p>
            </div>
            {% elif payment_method == 'transfer' %}
            <div style="text-align:center;padding:20px;">
                <p style="color:var(--gray-600);">请联系客服获取银行转账信息</p>
                <p style="font-size:0.85rem;color:var(--gray-400);margin-top:8px;">📧 admin@yigeworks.com</p>
                <a href="{% url 'shop:contact' %}" class="btn btn-outline btn-sm mt-4">联系我们</a>
            </div>
            {% endif %}
        </div>

        <div style="text-align:center;margin-top:16px;">
            <a href="{% url 'shop:contact' %}" style="color:var(--gray-400);font-size:0.85rem;">遇到问题？联系我们</a>
        </div>
    </div>
</section>

{% if payment_method == 'paypal' %}
<script>
paypal_sdk.Buttons({
    style: { layout: 'vertical', color: 'gold', shape: 'rect', label: 'paypal', height: 45 },
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    currency_code: '{{ order.currency }}',
                    value: '{{ order.total_paid|stringformat:"f" }}',
                    breakdown: { item_total: { currency_code: '{{ order.currency }}', value: '{{ order.total_paid|stringformat:"f" }}' } }
                },
                { reference_id: 'ORDER-{{ order.id }}' }]
        });
    },
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            fetch('{% url "payment:paypal_capture" %}', {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}'},
                body: JSON.stringify({orderID: data.orderID})
            }).then(r => r.json()).then(d => {
                if (d.status === 'ok') {
                    window.location.href = '{% url "payment:success" %}?order_id=' + d.order_id;
                } else {
                    alert('支付处理失败，请联系客服');
                }
            });
        });
    },
    onCancel: function() {
        window.location.href = '{% url "payment:cancelled" %}';
    },
    onError: function(err) {
        alert('支付出错: ' + err);
    }
}).render('#paypal-button-container');
</script>
{% endif %}
{% endblock %}
''')

# ========== 7. Payment Success ==========
write('payment/templates/payment/success.html', '''{% extends "base.html" %}

{% block title %}支付成功 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:640px;text-align:center;">
        <div style="font-size:5rem;margin-bottom:24px;">🎉</div>
        <h1 class="section-title" style="color:var(--green);">支付成功！</h1>
        <p style="color:var(--gray-500);font-size:1.1rem;margin-bottom:32px;">感谢您的购买！我们将尽快为您开通课程访问权限。</p>

        <div class="card" style="text-align:left;">
            <h3 style="margin-bottom:16px;">接下来您可以：</h3>
            <ul style="padding-left:0;">
                <li style="padding:12px 0;border-bottom:1px solid var(--gray-100);display:flex;align-items:center;gap:12px;">
                    <span style="color:var(--green);">✓</span>
                    <span>查收确认邮件（包含订单详情和访问链接）</span>
                </li>
                <li style="padding:12px 0;border-bottom:1px solid var(--gray-100);display:flex;align-items:center;gap:12px;">
                    <span style="color:var(--green);">✓</span>
                    <span>通过邮箱查询订单历史</span>
                </li>
                <li style="padding:12px 0;display:flex;align-items:center;gap:12px;">
                    <span style="color:var(--green);">✓</span>
                    <span>如有问题随时联系客服 admin@yigeworks.com</span>
                </li>
            </ul>
        </div>

        <div style="display:flex;gap:16px;justify-content:center;margin-top:32px;flex-wrap:wrap;">
            <a href="{% url 'shop:home' %}" class="btn btn-primary">返回首页</a>
            <a href="{% url 'orders:history' %}" class="btn btn-outline">查询订单</a>
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 8. Payment Cancelled ==========
write('payment/templates/payment/cancelled.html', '''{% extends "base.html" %}

{% block title %}支付取消 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:640px;text-align:center;">
        <div style="font-size:5rem;margin-bottom:24px;">😢</div>
        <h1 class="section-title">支付已取消</h1>
        <p style="color:var(--gray-500);font-size:1.1rem;margin-bottom:32px;">您的订单已取消，您可以随时重新下单。</p>
        <div style="display:flex;gap:16px;justify-content:center;">
            <a href="{% url 'shop:product_list' %}" class="btn btn-primary">重新选购</a>
            <a href="{% url 'shop:contact' %}" class="btn btn-outline">联系客服</a>
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 9. Order Confirmation ==========
write('orders/templates/orders/order_confirmation.html', '''{% extends "base.html" %}

{% block title %}订单确认 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:800px;">
        <div style="text-align:center;margin-bottom:40px;">
            <div style="font-size:4rem;">📋</div>
            <h1 class="section-title">订单已创建</h1>
            <p style="color:var(--gray-500);">订单号：<strong>#{{ order.id }}</strong></p>
        </div>

        <div class="card">
            <h3 style="margin-bottom:16px;">订单详情</h3>
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="border-bottom:2px solid var(--gray-200);">
                        <th style="text-align:left;padding:12px 8px;">商品</th>
                        <th style="text-align:center;padding:12px 8px;">数量</th>
                        <th style="text-align:right;padding:12px 8px;">小计</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in order.items.all %}
                    <tr style="border-bottom:1px solid var(--gray-100);">
                        <td style="padding:12px 8px;">{{ item.product_name }}</td>
                        <td style="text-align:center;padding:12px 8px;">{{ item.quantity }}</td>
                        <td style="text-align:right;padding:12px 8px;font-weight:600;">${{ item.total }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="2" style="padding:16px 8px;text-align:right;font-size:1.1rem;font-weight:700;">总计</td>
                        <td style="padding:16px 8px;text-align:right;font-size:1.1rem;font-weight:700;color:var(--primary);">${{ order.total_paid }}</td>
                    </tr>
                </tfoot>
            </table>
        </div>

        <div class="card mt-4">
            <h3 style="margin-bottom:12px;">收货信息</h3>
            <p>{{ order.display_name }} | {{ order.email }}</p>
            {% if order.company %}<p>{{ order.company }}</p>{% endif %}
            {% if order.phone %}<p>{{ order.phone }}</p>{% endif %}
            <p style="margin-top:8px;color:var(--gray-400);font-size:0.85rem;">支付方式：{{ order.get_payment_method_display }}</p>
        </div>

        <div style="text-align:center;margin-top:32px;">
            <a href="{% url 'payment:process' order.payment_method %}" class="btn btn-accent btn-lg">立即支付 ${{ order.total_paid }}</a>
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 10. Order History ==========
write('orders/templates/orders/order_list.html', '''{% extends "base.html" %}

{% block title %}订单查询 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:800px;">
        <h1 class="section-title">订单查询</h1>
        <p class="section-subtitle">输入购买时使用的邮箱查询订单历史</p>

        <form method="get" class="card" style="display:flex;gap:12px;margin-bottom:32px;">
            <input type="email" name="email" value="{{ email }}" class="form-input" placeholder="输入您的邮箱" required style="flex:1;">
            <button type="submit" class="btn btn-primary">查询</button>
        </form>

        {% if orders %}
        <div>
            {% for order in orders %}
            <div class="card" style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                    <div>
                        <h3 style="font-size:1.1rem;">订单 #{{ order.id }}</h3>
                        <p style="font-size:0.85rem;color:var(--gray-400);">{{ order.created|date:"Y-m-d H:i" }}</p>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.2rem;font-weight:700;color:var(--primary);">${{ order.total_paid }}</div>
                        {% if order.status == 'paid' %}
                        <span class="tag tag-green">已支付</span>
                        {% elif order.status == 'pending' %}
                        <span class="tag tag-amber">待支付</span>
                        {% else %}
                        <span class="tag tag-blue">{{ order.get_status_display }}</span>
                        {% endif %}
                    </div>
                </div>
                <div style="margin-top:12px;border-top:1px solid var(--gray-100);padding-top:12px;">
                    {% for item in order.items.all %}
                    <span style="font-size:0.9rem;color:var(--gray-600);">{{ item.product_name }} x{{ item.quantity }}{% if not forloop.last %}，{% endif %}</span>
                    {% endfor %}
                </div>
                {% if order.status == 'paid' %}
                <a href="#" class="btn btn-sm btn-green mt-4">访问课程</a>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% elif email %}
        <div class="card" style="text-align:center;padding:40px;">
            <p style="color:var(--gray-500);">未找到使用此邮箱的订单</p>
        </div>
        {% endif %}
    </div>
</section>
{% endblock %}
''')

# ========== 11. Order Detail ==========
write('orders/templates/orders/order_detail.html', '''{% extends "base.html" %}

{% block title %}订单 #{{ order.id }} | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:800px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;">
            <h1>订单 #{{ order.id }}</h1>
            {% if order.status == 'pending' %}
            <a href="{% url 'payment:process' order.payment_method %}" class="btn btn-accent">去支付</a>
            {% elif order.status == 'paid' %}
            <span class="tag tag-green" style="font-size:1rem;padding:8px 16px;">已支付</span>
            {% endif %}
        </div>

        <div class="card">
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr style="border-bottom:2px solid var(--gray-200);">
                    <th style="text-align:left;padding:12px;">商品</th>
                    <th style="text-align:center;padding:12px;">数量</th>
                    <th style="text-align:right;padding:12px;">小计</th>
                </tr></thead>
                <tbody>
                    {% for item in order.items.all %}
                    <tr style="border-bottom:1px solid var(--gray-100);">
                        <td style="padding:12px;">{{ item.product_name }}</td>
                        <td style="text-align:center;padding:12px;">{{ item.quantity }}</td>
                        <td style="text-align:right;padding:12px;">${{ item.total }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot><tr>
                    <td colspan="2" style="padding:16px;text-align:right;font-size:1.1rem;font-weight:700;">总计</td>
                    <td style="text-align:right;padding:16px;font-size:1.1rem;font-weight:700;color:var(--primary);">${{ order.total_paid }}</td>
                </tr></tfoot>
            </table>
        </div>

        <div class="card mt-4">
            <h3 style="margin-bottom:12px;">订单信息</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.9rem;">
                <div><span style="color:var(--gray-400);">姓名：</span>{{ order.display_name }}</div>
                <div><span style="color:var(--gray-400);">邮箱：</span>{{ order.email }}</div>
                <div><span style="color:var(--gray-400);">公司：</span>{{ order.company|default:"-" }}</div>
                <div><span style="color:var(--gray-400);">电话：</span>{{ order.phone|default:"-" }}</div>
                <div><span style="color:var(--gray-400);">支付方式：</span>{{ order.get_payment_method_display }}</div>
                <div><span style="color:var(--gray-400);">状态：</span>{{ order.get_status_display }}</div>
                <div><span style="color:var(--gray-400);">创建时间：</span>{{ order.created|date:"Y-m-d H:i" }}</div>
                {% if order.paypal_order_id %}
                <div><span style="color:var(--gray-400);">PayPal订单号：</span>{{ order.paypal_order_id }}</div>
                {% endif %}
            </div>
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 12. Pricing ==========
write('shop/templates/shop/pricing.html', '''{% extends "base.html" %}

{% block title %}定价方案 | YigeWorks{% endblock %}

{% block content %}
<section class="hero" style="padding:80px 0;">
    <div class="container" style="text-align:center;">
        <h1>选择适合您的方案</h1>
        <p style="opacity:0.9;font-size:1.1rem;margin-top:12px;">从自学到企业定制，满足不同阶段的安全合规需求</p>
    </div>
</section>

<section class="section" style="margin-top:-40px;">
    <div class="container">
        <div class="pricing-grid">
            {% for product in products %}
            <div class="pricing-card {% if product.is_featured %}featured{% endif %}">
                <span class="tag tag-blue">{{ product.get_product_type_display }}</span>
                <h3 style="margin-top:8px;">{{ product.name }}</h3>
                <p class="plan-desc">{{ product.short_description }}</p>
                <div>
                    <span class="plan-price">${{ product.price }}</span>
                    {% if product.original_price > product.price %}
                    <span class="plan-original">原价 ${{ product.original_price }}</span>
                    {% endif %}
                </div>
                {% if product.duration %}
                <p style="margin-top:8px;color:var(--gray-400);font-size:0.9rem;">{{ product.duration }} · {{ product.modules }} 课时</p>
                {% endif %}
                <form method="post" action="{% url 'shop:cart_add' product.id %}">
                    {% csrf_token %}
                    <button type="submit" class="btn {% if product.is_featured %}btn-accent{% else %}btn-outline{% endif %} mt-8" style="width:100%;">立即购买</button>
                </form>
                <a href="{% url 'shop:product_detail' product.slug %}" style="display:block;text-align:center;margin-top:8px;font-size:0.85rem;color:var(--gray-400);">查看详情 →</a>
            </div>
            {% empty %}
            <div class="card" style="text-align:center;padding:60px;grid-column:1/-1;">
                <h3>方案即将上线</h3>
                <p style="color:var(--gray-500);">请稍后再来查看定价方案</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 13. About ==========
write('shop/templates/shop/about.html', '''{% extends "base.html" %}

{% block title %}关于专家 | YigeWorks{% endblock %}

{% block content %}
<section class="section">
    <div class="container" style="max-width:800px;">
        <div style="text-align:center;margin-bottom:48px;">
            <div style="width:120px;height:120px;border-radius:50%;background:var(--primary-light);margin:0 auto 24px;display:flex;align-items:center;justify-content:center;font-size:3rem;">👨‍🔬</div>
            <h1 class="section-title">30年安全环保实战专家</h1>
            <p style="color:var(--gray-500);font-size:1.1rem;">专注帮助中资出海企业实现安全与环境合规</p>
        </div>

        <div class="card mb-8">
            <h3 style="margin-bottom:16px;">专业资质</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ ISO 45001 主任审核员</div>
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ ISO 14001 内审员</div>
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ 注册安全工程师</div>
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ 消防工程师</div>
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ 设备风险辨识专家</div>
                <div style="padding:12px;background:var(--gray-50);border-radius:8px;">✓ 消防安全设计与验收</div>
            </div>
        </div>

        <div class="card mb-8">
            <h3 style="margin-bottom:16px;">服务领域</h3>
            <ul style="padding-left:0;">
                <li style="padding:8px 0;border-bottom:1px solid var(--gray-100);">🏗️ 东南亚/非洲中资工厂安全合规体系建设</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--gray-100);">📋 ISO 45001+ISO 14001 双体系落地辅导</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--gray-100);">⚙️ 设备风险辨识与安全评估</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--gray-100);">🔥 消防安全设计与验收咨询</li>
                <li style="padding:8px 0;">📊 安全培训与企业内训</li>
            </ul>
        </div>

        <div style="text-align:center;">
            <a href="{% url 'shop:product_list' %}" class="btn btn-primary btn-lg">查看课程产品</a>
            <a href="{% url 'shop:contact' %}" class="btn btn-outline btn-lg" style="margin-left:12px;">联系咨询</a>
        </div>
    </div>
</section>
{% endblock %}
''')

# ========== 14. Privacy ==========
write('shop/templates/shop/privacy.html', '''{% extends "base.html" %}
{% block title %}隐私政策 | YigeWorks{% endblock %}
{% block content %}
<section class="section"><div class="container" style="max-width:800px;">
    <h1 class="section-title">隐私政策</h1>
    <div class="card" style="line-height:2;color:var(--gray-600);">
        <p><strong>生效日期：</strong>2024年1月1日</p>
        <h3 style="margin:24px 0 12px;">1. 信息收集</h3>
        <p>我们收集您在购买课程或服务时提供的个人信息，包括姓名、邮箱、公司名称和电话号码。我们使用这些信息来处理订单、提供客户服务并发送相关通知。</p>
        <h3 style="margin:24px 0 12px;">2. 信息使用</h3>
        <p>您的信息仅用于：订单处理、课程交付、客户支持、服务改进。我们不会将您的个人信息出售或分享给第三方。</p>
        <h3 style="margin:24px 0 12px;">3. 支付安全</h3>
        <p>所有支付交易通过 PayPal 安全处理，我们不存储您的信用卡或银行账户信息。</p>
        <h3 style="margin:24px 0 12px;">4. Cookie</h3>
        <p>我们使用 Cookie 来改善您的浏览体验和分析网站流量。您可以通过浏览器设置管理 Cookie 偏好。</p>
        <h3 style="margin:24px 0 12px;">5. 联系我们</h3>
        <p>如有隐私相关问题，请联系：admin@yigeworks.com</p>
    </div>
</div></section>
{% endblock %}
''')

# ========== 15. Terms ==========
write('shop/templates/shop/terms.html', '''{% extends "base.html" %}
{% block title %}服务条款 | YigeWorks{% endblock %}
{% block content %}
<section class="section"><div class="container" style="max-width:800px;">
    <h1 class="section-title">服务条款</h1>
    <div class="card" style="line-height:2;color:var(--gray-600);">
        <p><strong>生效日期：</strong>2024年1月1日</p>
        <h3 style="margin:24px 0 12px;">1. 服务说明</h3>
        <p>YigeWorks 提供在线安全培训课程、文件模板和咨询服务。购买后您将获得对应产品的访问权限。</p>
        <h3 style="margin:24px 0 12px;">2. 退款政策</h3>
        <p>课程购买后 7 天内，若课程进度未超过 30%，可申请全额退款。超过 7 天或进度超过 30% 的订单不予退款。</p>
        <h3 style="margin:24px 0 12px;">3. 知识产权</h3>
        <p>所有课程内容、模板文件均为 YigeWorks 独家所有。购买后您获得个人使用授权，不得复制、分发或转售。</p>
        <h3 style="margin:24px 0 12px;">4. 免责声明</h3>
        <p>课程内容仅供学习和参考，不构成法律意见。实际应用请结合当地法律法规和具体情况。</p>
        <h3 style="margin:24px 0 12px;">5. 联系</h3>
        <p>服务条款相关问题请联系：admin@yigeworks.com</p>
    </div>
</div></section>
{% endblock %}
''')

print('\\n所有模板文件生成完成！')
