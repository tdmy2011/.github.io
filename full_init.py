"""Upload and run scripts on server to create superuser and init data."""
import paramiko, sys, io, time

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

def upload_script(name, content):
    remote = f'{RDIR}/{name}'
    with sftp.open(remote, 'w') as f:
        f.write(content)
    print(f'  Uploaded: {name}')

# 1. Create superuser script
superuser_script = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'yjurado860@gmail.com', 'Yige2026@')
    print('CREATED: admin / Yige2026@')
else:
    print('EXISTS: admin already exists')
count = User.objects.filter(is_superuser=True).count()
print(f'Superuser count: {count}')
'''

upload_script('_create_superuser.py', superuser_script)
run(f'cd {RDIR} && venv/bin/python _create_superuser.py', 'create superuser')

# 2. Check init_data.py output
print('\n=== Checking init_data.py output ===')
out, err = run(f'cd {RDIR} && venv/bin/python init_data.py 2>&1')
if not out.strip() and not err.strip():
    print('  No output - let me check if the file exists and its structure')
    run(f'ls -la {RDIR}/init_data.py 2>&1', 'init_data.py file')
    run(f'head -5 {RDIR}/init_data.py 2>&1', 'init_data.py head')

# 3. If init_data.py failed, create our own init script
init_script = '''#!/usr/bin/env python
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'yigeworks.settings'
django.setup()

from django.core.management import call_command

# Run init_data management command style - directly create objects
from pages.models import SiteConfig, HeroBanner, FAQ, Testimonial, ServiceRegion
from products.models import Category, Product
from blog.models import PostCategory, Tag, Post

# SiteConfig
sc, created = SiteConfig.objects.get_or_create(
    defaults={
        'site_name': 'YigeWorks HSE Consulting',
        'contact_email': 'yjurado860@gmail.com',
        'phone_hk': '+852-XXXX-XXXX',
        'wechat1': 'YigeWorks',
        'working_hours': 'Mon-Fri 9:00-18:00 (HKT)',
        'copyright_text': '2024-2026 YigeWorks. All rights reserved.',
    }
)
print(f'SiteConfig: {"created" if created else "exists"} id={sc.id}')

# Categories
cats = [
    ('courses', '培训课程', 'Training Courses', '\\U0001f3eb', 1),
    ('templates', '文档模板', 'Document Templates', '\\U0001f4c4', 2),
    ('consulting', '咨询服务', 'Consulting Services', '\\U0001f91d', 3),
    ('tools', '自评工具', 'Self-Assessment Tools', '\\U0001f527', 4),
]
for slug, name_zh, name_en, icon, order in cats:
    c, cr = Category.objects.get_or_create(slug=slug, defaults={'name_zh': name_zh, 'name_en': name_en, 'icon': icon, 'order': order})
    print(f'  Category: {slug} {"created" if cr else "exists"}')

# Products
products_data = [
    ('iso45001-lead-auditor', 'ISO 45001内审员课程', 'ISO 45001 Lead Auditor Course', 'courses',
     '深入学习ISO 45001:2018标准要求，掌握内审流程与技巧，成为合格的安全管理体系内审员。', 
     'Deep dive into ISO 45001:2018, master internal audit processes.',
     '5天系统培训\\n实战案例分析\\n内审员证书', 2980, 450, 428),
    ('iso14001-lead-auditor', 'ISO 14001内审员课程', 'ISO 14001 Lead Auditor Course', 'courses',
     '全面学习ISO 14001:2015环境管理体系标准，掌握环境因素识别与合规性评价方法。',
     'Comprehensive ISO 14001:2015 EMS training.',
     '5天系统培训\\n环境因素识别\\n合规评价方法', 2980, 450, 428),
    ('ohsas-transition', 'OHSAS 18001转ISO 45001', 'OHSAS to ISO 45001 Transition', 'courses',
     '帮助企业从OHSAS 18001平稳过渡到ISO 45001标准，确保体系连续性。',
     'Smooth transition from OHSAS 18001 to ISO 45001.',
     '差异分析\\n体系升级指导\\n文件更新', 1980, 350, 285),
    ('hse-advanced', 'HSE高级管理课程', 'HSE Advanced Management', 'courses',
     '面向HSE经理的高阶课程，涵盖风险评估、事故调查、安全文化建设等核心主题。',
     'Advanced HSE management for safety managers.',
     '风险评估\\n事故调查\\n安全文化建设', 3980, 580, 571),
    ('safety-manual-template', '安全手册模板', 'Safety Manual Template', 'templates',
     'ISO 45001安全管理体系手册模板，可直接使用和修改，包含全套管理文件。',
     'ISO 45001 safety manual template, ready to use.',
     '完整手册模板\\n程序文件\\n作业指导书', 680, 128, 98),
    ('ems-manual-template', '环境管理手册模板', 'EMS Manual Template', 'templates',
     'ISO 14001环境管理体系手册模板，适用于制造业和工程建设企业。',
     'ISO 14001 EMS manual for manufacturing and construction.',
     'EMS手册\\n环境因素清单\\n合规评价表', 680, 128, 98),
    ('risk-assessment-template', '风险评估模板包', 'Risk Assessment Template Pack', 'templates',
     'JSA工作安全分析+风险评估矩阵全套模板，覆盖常见高风险作业。',
     'JSA + Risk Assessment Matrix templates.',
     'JSA模板\\n风险矩阵\\n高风险作业清单', 480, 88, 68),
    ('iso45001-consulting', 'ISO 45001认证咨询', 'ISO 45001 Certification Consulting', 'consulting',
     '从零到认证，30天快速落地ISO 45001安全管理体系。含文件编制、培训、内审、外审支持。',
     'Zero to certified in 30 days with full support.',
     '体系诊断\\n文件编制\\n内审支持\\n外审辅导', 19800, 3500, 2836),
    ('iso14001-consulting', 'ISO 14001认证咨询', 'ISO 14001 Certification Consulting', 'consulting',
     '专业环境管理体系认证辅导，帮助企业通过ISO 14001认证审核。',
     'Professional ISO 14001 certification consulting.',
     '环境因素识别\\n合规性评价\\n文件编制', 19800, 3500, 2836),
    ('dual-system-consulting', 'ISO 45001+14001双体系', 'Dual System Consulting', 'consulting',
     '同时建立和实施ISO 45001+14001双体系，最大化效率，降低认证成本。',
     'Implement both ISO 45001 and 14001 simultaneously.',
     '双体系整合\\n一体化文件\\n联合审核', 32800, 5800, 4700),
    ('safety-culture-assessment', '安全文化自评工具', 'Safety Culture Assessment', 'tools',
     '基于国际标准的安全文化评估问卷，快速诊断企业安全管理成熟度。',
     'Safety culture assessment tool based on international standards.',
     '在线评估问卷\\n自动评分\\n改进建议', 980, 188, 148),
    ('compliance-checker', '合规性检查工具', 'Compliance Checker', 'tools',
     '东南亚/非洲主要国家HSE法规合规性自动检查工具，一键生成合规报告。',
     'HSE compliance checker for SE Asia and Africa.',
     '法规数据库\\n自动检查\\n合规报告', 1480, 288, 228),
]
for slug, name_zh, name_en, cat_slug, desc_zh, desc_en, feat_zh, price_cny, price_usd, disc_usd in products_data:
    cat = Category.objects.get(slug=cat_slug)
    p, cr = Product.objects.get_or_create(slug=slug, defaults={
        'name_zh': name_zh, 'name_en': name_en, 'category': cat, 'product_type': cat_slug,
        'description_zh': desc_zh, 'description_en': desc_en,
        'features_zh': feat_zh, 'features_en': feat_zh.replace('\\\\n', '\\n'),
        'price_cny': price_cny, 'price_usd': price_usd, 'discount_price_usd': disc_usd,
        'is_active': True, 'is_featured': True, 'stock': 999,
    })
    print(f'  Product: {slug} {"created" if cr else "exists"}')

# Blog categories
blog_cats = [
    ('hse-news', 'HSE资讯', 'HSE News'),
    ('case-study', '案例分析', 'Case Studies'),
    ('compliance', '合规指南', 'Compliance Guide'),
    ('safety-culture', '安全文化', 'Safety Culture'),
]
for slug, name_zh, name_en in blog_cats:
    c, cr = PostCategory.objects.get_or_create(slug=slug, defaults={'name_zh': name_zh, 'name_en': name_en})
    print(f'  BlogCat: {slug} {"created" if cr else "exists"}')

# Tags
tags_data = ['ISO45001', 'ISO14001', '东南亚', '非洲', '风险评估', '安全培训', '合规', '审核', '中资企业', '出海']
for t in tags_data:
    tag, cr = Tag.objects.get_or_create(name=t)
    print(f'  Tag: {t} {"created" if cr else "exists"}')

# Blog posts
posts_data = [
    ('hse-trends-2024', '2024年HSE管理十大趋势', 'Top 10 HSE Trends in 2024', 'hse-news',
     '数字化安全管理、AI风险评估、远程审核等新兴趋势正在重塑HSE行业...',
     'Digital safety, AI risk assessment, and remote auditing reshape the HSE industry...',
     ['ISO45001', '安全培训']),
    ('se-asia-compliance', '东南亚HSE合规指南', 'SE Asia HSE Compliance Guide', 'compliance',
     '越南、泰国、印尼、马来西亚等国的HSE法规要点和合规建议...',
     'HSE regulations and compliance tips for Vietnam, Thailand, Indonesia, Malaysia...',
     ['合规', '东南亚']),
    ('iso-certification-guide', 'ISO认证快速落地指南', 'ISO Certification Quick Guide', 'hse-news',
     '30天快速通过ISO 45001/14001认证的关键步骤和常见陷阱...',
     'Key steps and common pitfalls for ISO 45001/14001 certification in 30 days...',
     ['ISO45001', 'ISO14001', '审核']),
    ('safety-culture-build', '如何构建安全文化', 'Building a Strong Safety Culture', 'safety-culture',
     '安全文化不是口号，而是从管理层到一线员工的系统性变革...',
     'Safety culture is not a slogan, but systematic change from management to frontline...',
     ['安全文化', '中资企业']),
]
for slug, title_zh, title_en, cat_slug, excerpt_zh, excerpt_en, tag_names in posts_data:
    cat = PostCategory.objects.get(slug=cat_slug)
    tags = Tag.objects.filter(name__in=tag_names)
    p, cr = Post.objects.get_or_create(slug=slug, defaults={
        'title_zh': title_zh, 'title_en': title_en, 'category': cat,
        'excerpt_zh': excerpt_zh, 'excerpt_en': excerpt_en,
        'content_zh': f'<p>{excerpt_zh}</p><p>这是一篇详细的{title_zh}文章，请访问完整页面查看更多内容。</p>',
        'content_en': f'<p>{excerpt_en}</p><p>This is a detailed article about {title_en}.</p>',
        'author': 'Admin', 'status': 'published', 'is_featured': True,
    })
    if cr:
        p.tags.set(tags)
        print(f'  Post: {slug} created with {len(tag_names)} tags')
    else:
        print(f'  Post: {slug} exists')

# FAQs
faqs = [
    ('ISO 45001认证需要多长时间？', '通常需要30-90天，取决于企业现有体系基础。我们提供30天快速落地服务。',
     'How long does ISO 45001 certification take?', 'Typically 30-90 days. We offer 30-day fast-track service.', 'certification'),
    ('东南亚国家的HSE法规与中国有什么不同？', '各国法规差异较大，如越南有严格的劳保法规、印尼要求SMK3认证等。',
     'How do SE Asia HSE regulations differ from China?', 'Regulations vary significantly across countries.', 'compliance'),
    ('你们的咨询服务包含什么？', '从体系诊断、文件编制、员工培训到内审外审辅导的全流程服务。',
     'What does your consulting service include?', 'Full service from diagnosis to certification.', 'service'),
]
for i, (q_zh, a_zh, q_en, a_en, cat) in enumerate(faqs):
    f, cr = FAQ.objects.get_or_create(question_zh=q_zh, defaults={
        'answer_zh': a_zh, 'question_en': q_en, 'answer_en': a_en, 'category': cat, 'order': i+1
    })
    print(f'  FAQ: {q_zh[:20]}... {"created" if cr else "exists"}')

# Service regions
regions = [
    ('越南 Vietnam', 'southeast_asia', '劳动安全法', 'ISO认证,安全培训,风险评估'),
    ('泰国 Thailand', 'southeast_asia', '泰国安全法规', 'ISO认证,安全培训,合规咨询'),
    ('印尼 Indonesia', 'southeast_asia', 'SMK3法规', 'ISO认证,安全培训,风险评估'),
    ('马来西亚 Malaysia', 'southeast_asia', 'OSHA 1994', 'ISO认证,合规咨询'),
    ('菲律宾 Philippines', 'southeast_asia', 'DOLE法规', '安全培训,合规咨询'),
    ('缅甸 Myanmar', 'southeast_asia', '工厂法', '安全培训'),
    ('柬埔寨 Cambodia', 'southeast_asia', '劳动法', '安全培训'),
    ('老挝 Laos', 'southeast_asia', '劳动法', '安全培训'),
    ('新加坡 Singapore', 'southeast_asia', 'WSH法案', 'ISO认证,安全培训'),
    ('尼日利亚 Nigeria', 'africa', 'NIOSH法规', 'ISO认证,安全培训'),
    ('肯尼亚 Kenya', 'africa', 'OSHA法案', '安全培训,合规咨询'),
    ('坦桑尼亚 Tanzania', 'africa', 'OSHA法规', '安全培训'),
    ('埃塞俄比亚 Ethiopia', 'africa', '劳动法', '安全培训'),
    ('加纳 Ghana', 'africa', '工厂法', '安全培训'),
    ('南非 South Africa', 'africa', 'OHSA法案', 'ISO认证,安全培训,风险评估'),
    ('中国大陆 China', 'greater_china', '安全生产法', 'ISO认证,安全培训,风险评估,合规咨询'),
    ('香港 Hong Kong', 'greater_china', '工厂及工业经营条例', '安全培训,风险评估'),
]
for name, region, regulations, services in regions:
    r, cr = ServiceRegion.objects.get_or_create(name=name, defaults={
        'region': region, 'regulations': regulations, 'services': services
    })
    print(f'  Region: {name} {"created" if cr else "exists"}')

print('\\n=== All initial data created! ===')
'''

upload_script('_init_all_data.py', init_script)
run(f'cd {RDIR} && venv/bin/python _init_all_data.py 2>&1', 'init all data')

# 4. Debug /shop/cart/ 500 error
print('\n=== Debug cart 500 ===')
out, err = run(f'curl -s http://localhost:80/shop/cart/ 2>&1 | tail -20', 'cart response')

# Check django error logs
run(f'cd {RDIR} && venv/bin/python manage.py shell -c "from shop.views import cart_detail; print(cart_detail)" 2>&1', 'import cart view')

# Try to find the actual error
run(f'cd {RDIR} && DJANGO_SETTINGS_MODULE=yigeworks.settings venv/bin/python -c "'
    'import django; django.setup();'
    'from django.test import RequestFactory; from shop.views import cart_detail;'
    'rf = RequestFactory();'
    'req = rf.get(\"/shop/cart/\");'
    'try: resp = cart_detail(req); print(f\"Status: {resp.status_code}\");'
    'except Exception as e: print(f\"Error: {e}\")'
    '" 2>&1', 'test cart view')

sftp.close()
ssh.close()
print('\nDone!')
