"""
批量生成所有缺失的 Django 模板和代码文件
"""
import os

BASE = 'C:/Users/Administrator/WorkBuddy/2026-05-31-11-24-40/yigeworks_shop'

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK: {path}')

# ========== 1. Order Form ==========
write('orders/forms.py', '''from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'company', 'phone', 'payment_method']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '名（First Name）'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '姓（Last Name）'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': '邮箱地址'}),
            'company': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '公司名称（选填）'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '手机号码（选填）'}),
            'payment_method': forms.Select(attrs={'class': 'form-input'}),
        }
''')

# ========== 2. Shop Admin ==========
write('shop/admin.py', '''from django.contrib import admin
from .models import Category, Product, Module, Lesson, FAQ, Newsletter, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    ordering = ['order']


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price', 'product_type', 'is_active', 'is_featured', 'created']
    list_filter = ['is_active', 'is_featured', 'product_type', 'category']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'price']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'product']
    list_filter = ['product']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'module', 'is_free', 'duration']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_zh', 'order', 'is_active']
    list_editable = ['is_active', 'order']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'source']
    search_fields = ['email']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'created', 'is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'message']
''')

# ========== 3. Orders Admin ==========
write('orders/admin.py', '''from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_name', 'email', 'total_paid', 'status', 'payment_method', 'created']
    list_filter = ['status', 'payment_method']
    search_fields = ['email', 'first_name', 'last_name']
    list_editable = ['status']
    inlines = [OrderItemInline]
    date_hierarchy = 'created'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'price', 'quantity']
''')

# ========== 4. Payment Admin ==========
write('payment/admin.py', '''from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_id', 'payment_method', 'amount', 'status', 'created']
    list_filter = ['status', 'payment_method']
    search_fields = ['payment_id', 'order__email']
''')

# ========== 5. Checkout View ==========
write('orders/views.py', '''from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from .models import Order, OrderItem
from .forms import OrderCreateForm
from shop.cart import Cart


def checkout(request):
    """结算页面"""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_paid = cart.get_total_price()
            order.currency = settings.PAYPAL_CURRENCY
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('payment:process', payment_method=order.payment_method)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
        'PAYPAL_CURRENCY': settings.PAYPAL_CURRENCY,
    })


def order_create(request):
    """创建订单（直接从购物车，不需要单独页面）"""
    return checkout(request)


class OrderListView(View):
    """订单确认页"""
    def get(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            return redirect('shop:home')
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order_confirmation.html', {'order': order})


class OrderHistoryView(View):
    """订单历史（通过邮箱查询）"""
    def get(self, request):
        email = request.GET.get('email', '')
        orders = []
        if email:
            orders = Order.objects.filter(email=email).order_by('-created')[:20]
        return render(request, 'orders/order_list.html', {
            'orders': orders,
            'email': email,
        })


def order_detail(request, order_id):
    """订单详情"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})
''')

# ========== 6. Orders URLs (updated) ==========
write('orders/urls.py', '''from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create/', views.order_create, name='order_create'),
    path('confirmation/', views.OrderListView.as_view(), name='confirmation'),
    path('history/', views.OrderHistoryView.as_view(), name='history'),
    path('<int:order_id>/', views.order_detail, name='detail'),
]
''')

# ========== 7. Shop Views (add cart AJAX) ==========
write('shop/views.py', '''from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Category, Product, Module, Lesson, FAQ
from .cart import Cart
from .forms import ContactForm, NewsletterForm


def home(request):
    """首页"""
    featured = Product.objects.filter(is_active=True, is_featured=True)[:6]
    categories = Category.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)[:6]
    all_products = Product.objects.filter(is_active=True)[:8]
    return render(request, 'shop/home.html', {
        'featured': featured,
        'categories': categories,
        'faqs': faqs,
        'all_products': all_products,
    })


def product_list(request, category_slug=None):
    """产品列表"""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None
    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'products': products,
        'category': category,
    })


def product_detail(request, slug):
    """产品详情"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    modules = Module.objects.filter(product=product).prefetch_related('lessons')
    related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'modules': modules,
        'related': related,
    })


def cart_detail(request):
    """购物车"""
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    """添加到购物车（支持AJAX）"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': len(cart),
            'message': f'{product.name} 已加入购物车',
        })
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    """移除购物车项（支持AJAX）"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'cart_count': len(cart)})
    return redirect('shop:cart_detail')


def cart_update(request, product_id):
    """更新购物车数量"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product, quantity=quantity, update_quantity=True)
    else:
        cart.remove(product)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': len(cart),
            'total': str(cart.get_total_price()),
        })
    return redirect('shop:cart_detail')


def cart_clear(request):
    """清空购物车"""
    cart = Cart(request)
    cart.clear()
    return redirect('shop:cart_detail')


def pricing(request):
    """定价方案"""
    products = Product.objects.filter(is_active=True, product_type='course')
    return render(request, 'shop/pricing.html', {'products': products})


def course_syllabus(request):
    """课程大纲"""
    products = Product.objects.filter(is_active=True, product_type='course')
    return render(request, 'shop/course.html', {'products': products})


def about(request):
    """关于专家"""
    return render(request, 'shop/about.html')


def privacy(request):
    return render(request, 'shop/privacy.html')


def terms(request):
    return render(request, 'shop/terms.html')


def contact(request):
    """联系表单"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok', 'message': '留言已提交！'})
        return JsonResponse({'status': 'error', 'message': str(form.errors)})
    return JsonResponse({'status': 'error', 'message': '请使用 POST 请求'})


def newsletter_signup(request):
    """邮件订阅"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok', 'message': '订阅成功！'})
        return JsonResponse({'status': 'error', 'message': '邮箱格式不正确'})
    return JsonResponse({'status': 'error', 'message': '请使用 POST 请求'})


def search(request):
    """搜索"""
    q = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True, name__icontains=q) if q else []
    return render(request, 'shop/product_list.html', {
        'products': products,
        'search_query': q,
        'categories': Category.objects.filter(is_active=True),
    })
''')

# ========== 8. Shop URLs (updated) ==========
write('shop/urls.py', '''from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('pricing/', views.pricing, name='pricing'),
    path('course/', views.course_syllabus, name='course_syllabus'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('search/', views.search, name='search'),
]
''')

# ========== 9. Payment Views (enhanced) ==========
write('payment/views.py', '''from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from .models import Payment
from orders.models import Order
import json, urllib.request, base64


def process_payment(request, payment_method):
    """支付处理页面"""
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('shop:home')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/process.html', {
        'order': order,
        'payment_method': payment_method,
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,
        'PAYPAL_CURRENCY': settings.PAYPAL_CURRENCY,
        'PAYPAL_SANDBOX': settings.PAYPAL_SANDBOX,
    })


def payment_success(request):
    """支付成功"""
    return render(request, 'payment/success.html')


def payment_cancelled(request):
    """支付取消"""
    return render(request, 'payment/cancelled.html')


class PayPalCreateView(View):
    """PayPal 创建订单 API（前端调用）"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = request.session.get('order_id')
            if not order_id:
                return JsonResponse({'status': 'error', 'message': 'No order'})
            order = get_object_or_404(Order, id=order_id)
            order.paypal_order_id = data.get('orderID', '')
            order.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class PayPalCaptureView(View):
    """PayPal 捕获支付 API"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = request.session.get('order_id')
            if not order_id:
                return JsonResponse({'status': 'error', 'message': 'No order'})
            order = get_object_or_404(Order, id=order_id)
            paypal_order_id = data.get('orderID', '')

            # 更新订单状态
            order.status = 'paid'
            order.paypal_order_id = paypal_order_id
            order.save()

            # 创建支付记录
            Payment.objects.create(
                order=order,
                payment_id=paypal_order_id,
                payment_method='paypal',
                amount=order.total_paid,
                status='completed',
            )

            del request.session['order_id']
            return JsonResponse({'status': 'ok', 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
''')

# ========== 10. Payment URLs (updated) ==========
write('payment/urls.py', '''from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('<str:payment_method>/', views.process_payment, name='process'),
    path('success/', views.payment_success, name='success'),
    path('cancelled/', views.payment_cancelled, name='cancelled'),
    path('paypal/create/', views.PayPalCreateView.as_view(), name='paypal_create'),
    path('paypal/capture/', views.PayPalCaptureView.as_view(), name='paypal_capture'),
]
''')

print('\\n所有 Python 文件生成完成！')
