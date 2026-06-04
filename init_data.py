from django.core.management.base import BaseCommand
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yigeworks.settings')


class Command(BaseCommand):
    help = '初始化网站数据（产品、分类、博客、FAQ 等）'

    def handle(self, *args, **options):
        from pages.models import SiteConfig, FAQ, Testimonial, ServiceRegion
        from products.models import Category, Product
        from blog.models import PostCategory, Tag, Post

        # 1. 站点配置
        config, _ = SiteConfig.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'YigeWorks HSE Consulting',
                'site_description': '30年安全环保实战专家，帮助中资出海企业30天完成ISO 45001+ISO 14001双体系落地。',
                'contact_email': 'yjurado860@gmail.com',
                'contact_email2': 'fjfacxy@163.com',
                'phone_hk': '00852-46664920',
                'wechat1': '18060522680',
                'wechat2': '13814839118',
                'working_hours': '周一至周五 9:00-18:00 (HKT)',
                'paypal_client_id': 'Abx9jaJI_yKFrGrq6JcqKH47vWRFOFZWUv8pORx-ZenstcwhaU8qDtReCfoEdzbFDCDrNy3VmnXt37BU',
                'ga4_id': '',
                'copyright_text': '2025 YigeWorks HSE Consulting. All Rights Reserved.',
            }
        )
        self.stdout.write('OK: SiteConfig')

        # 2. FAQ
        faqs_data = [
            ('ISO 45001认证需要多长时间？', 'How long does ISO 45001 certification take?',
             '一般30-90天，取决于企业规模和准备程度。我们的带教版课程专门设计为30天快速落地方案。', 'Typically 30-90 days depending on company size. Our guided course is designed for 30-day rapid deployment.', '认证流程'),
            ('你们的服务覆盖哪些国家？', 'Which countries do you serve?',
             '主要覆盖东南亚（越南、泰国、印尼、马来西亚等9国）和非洲（尼日利亚、肯尼亚等6国）及大中华区。', 'We cover 9 SE Asian countries, 6 African countries, and Greater China.', '服务范围'),
            ('课程是中文还是英文？', 'Are courses in Chinese or English?',
             '全部课程提供中英双语版本，适合跨国企业管理团队。', 'All courses available in bilingual Chinese and English.', '课程内容'),
            ('是否提供售后服务？', 'Do you provide after-sales support?',
             '所有付费课程均包含3个月免费答疑服务，企业版包含1年技术支持。', 'All paid courses include 3 months free Q&A. Enterprise edition includes 1 year technical support.', '售后支持'),
            ('如何获取ISO认证模板？', 'How to get ISO certification templates?',
             '购买后立即通过邮件发送下载链接，包含15份完整的程序文件模板。', 'Download link sent immediately after purchase. Includes 15 complete procedure document templates.', '产品购买'),
        ]
        for i, (q_zh, q_en, a_zh, a_en, cat) in enumerate(faqs_data):
            FAQ.objects.get_or_create(question_zh=q_zh, defaults={
                'question_en': q_en, 'answer_zh': a_zh, 'answer_en': a_en,
                'category': cat, 'order': i, 'is_active': True
            })
        self.stdout.write(f'OK: {len(faqs_data)} FAQs')

        # 3. 服务区域
        regions = [
            ('越南', 'Vietnam', 'southeast_asia', 'QSV/TCLL/VD/QCVN 等法规'),
            ('泰国', 'Thailand', 'southeast_asia', 'OSHA Thailand, Factory Act'),
            ('印尼', 'Indonesia', 'southeast_asia', 'UU No.1/1970, K3法规'),
            ('马来西亚', 'Malaysia', 'southeast_asia', 'OSHA 1994, FMA 1967'),
            ('菲律宾', 'Philippines', 'southeast_asia', 'OSHA Standards, DOLE法规'),
            ('缅甸', 'Myanmar', 'southeast_asia', 'Factories Act'),
            ('柬埔寨', 'Cambodia', 'southeast_asia', 'Labour Law'),
            ('老挝', 'Laos', 'southeast_asia', 'Labour Law'),
            ('新加坡', 'Singapore', 'southeast_asia', 'WSH Act, MOM法规'),
            ('尼日利亚', 'Nigeria', 'africa', 'Factories Act, NIOSH'),
            ('肯尼亚', 'Kenya', 'africa', 'OSHA 2007'),
            ('埃塞俄比亚', 'Ethiopia', 'africa', 'Labour Proclamation'),
            ('坦桑尼亚', 'Tanzania', 'africa', 'OSHA Act 2003'),
            ('南非', 'South Africa', 'africa', 'OHS Act 85 of 1993'),
            ('埃及', 'Egypt', 'africa', 'Labour Law No.12/2003'),
            ('中国大陆', 'Mainland China', 'greater_china', '安全生产法, GB标准'),
            ('香港', 'Hong Kong', 'greater_china', 'OSHO, Factories and Industrial Undertakings Ordinance'),
        ]
        services = 'ISO认证,风险评估,安全培训,法规咨询,程序文件编写'
        for name_zh, name_en, rtype, regs in regions:
            ServiceRegion.objects.get_or_create(name_zh=name_zh, defaults={
                'name_en': name_en, 'region_type': rtype, 'regulations': regs,
                'services': services, 'is_active': True
            })
        self.stdout.write(f'OK: {len(regions)} ServiceRegions')

        # 4. 产品分类
        categories = [
            ('培训课程', 'Training Courses', 'course', '📚'),
            ('模板文档', 'Document Templates', 'template', '📄'),
            ('咨询服务', 'Consulting Services', 'consulting', '💼'),
            ('自查工具', 'Self-Assessment Tools', 'tool', '✅'),
        ]
        for name_zh, name_en, slug, icon in categories:
            Category.objects.get_or_create(slug=slug, defaults={
                'name_zh': name_zh, 'name_en': name_en, 'icon': icon
            })
        self.stdout.write(f'OK: {len(categories)} Categories')

        # 5. 产品
        course_cat = Category.objects.get(slug='course')
        template_cat = Category.objects.get(slug='template')
        consulting_cat = Category.objects.get(slug='consulting')
        tool_cat = Category.objects.get(slug='tool')

        products = [
            # 培训课程
            ('ISO双体系落地营（带教版）', 'ISO Dual System Bootcamp (Guided)', 'iso-dual-guided',
             course_cat, 'course', 1298, 179,
             '30天1对1带教，ISO 45001+ISO 14001双体系完整落地方案。包含：12节视频课+8次直播答疑+全套程序文件模板+专属微信群。',
             '30-day 1-on-1 coaching for ISO 45001+ISO 14001 dual system implementation. 12 video lessons + 8 live Q&A sessions + all templates.',
             '12节视频课（中英双语字幕）\n8次直播答疑\n全套15份程序文件模板\n专属微信答疑群\n30天完成认证准备',
             '12 video lessons (bilingual subtitles)\n8 live Q&A sessions\n15 procedure document templates\nPrivate WeChat group\n30-day certification readiness',
             True, True),
            ('ISO双体系落地营（自学版）', 'ISO Dual System (Self-Study)', 'iso-dual-self',
             course_cat, 'course', 499, 69,
             '自学完成ISO 45001+ISO 14001双体系建设。包含：12节视频课+PDF课件+全套程序文件模板。',
             'Self-study ISO 45001+ISO 14001 dual system. 12 video lessons + PDF courseware + all templates.',
             '12节视频课（中英双语字幕）\nPDF课件和讲义\n全套15份程序文件模板\n终身回看',
             '12 video lessons (bilingual subtitles)\nPDF courseware\n15 procedure document templates\nLifetime access',
             False, True),
            ('设备风险辨识专项课', 'Equipment Risk Identification Course', 'equip-risk-course',
             course_cat, 'course', 698, 97,
             '系统学习设备风险辨识方法，涵盖机械伤害、电气风险、高处作业等7大风险类别。',
             'Systematic equipment risk identification covering 7 major risk categories.',
             '7大风险类别详解\n风险辨识工具包\n30+真实案例分析\n实操练习题库',
             '7 risk categories explained\nRisk identification toolkit\n30+ real case studies\nPractice exercises',
             False, False),
            ('消防安全设计专项课', 'Fire Safety Design Course', 'fire-safety-course',
             course_cat, 'course', 598, 83,
             '掌握工厂消防安全设计核心要点，包括消防分区、逃生通道、灭火系统选型等。',
             'Master factory fire safety design essentials including fire zones, escape routes, and fire suppression systems.',
             '消防法规核心要点\n消防分区设计方法\n逃生通道规划\n灭火系统选型指南',
             'Fire regulation essentials\nFire zone design methods\nEscape route planning\nFire suppression system selection',
             False, False),
            # 模板文档
            ('ISO 45001全套15份模板', 'ISO 45001 Full 15 Templates', 'iso45001-templates',
             template_cat, 'template', 399, 55,
             '15份完整的ISO 45001程序文件模板（Word格式），可直接修改使用。',
             '15 complete ISO 45001 procedure document templates (Word format), ready for customization.',
             '15份Word格式模板\n涵盖全部核心条款\n中英双语版本\n附填写说明',
             '15 Word format templates\nAll core clauses covered\nBilingual version\nWith filling instructions',
             False, True),
            ('ISO 14001环境管理体系模板', 'ISO 14001 EMS Templates', 'iso14001-templates',
             template_cat, 'template', 299, 42,
             'ISO 14001环境管理体系全套程序文件模板，包含环境因素识别、合规评价等核心文件。',
             'Complete ISO 14001 EMS procedure document templates.',
             '环境因素识别\n合规性评价\n环境目标管理\n应急准备与响应',
             'Environmental aspect identification\nCompliance evaluation\nEnvironmental objectives\nEmergency preparedness',
             False, False),
            ('东南亚法规对照手册', 'SE Asia Regulation Handbook', 'sea-regulation-handbook',
             template_cat, 'template', 199, 28,
             '东南亚9国安全法规与中国标准对照手册，帮助企业快速了解当地合规要求。',
             'Regulation comparison handbook for 9 SE Asian countries vs Chinese standards.',
             '9国法规对照\n关键差异标注\n合规检查清单\n更新服务（1年）',
             '9-country regulation comparison\nKey differences marked\nCompliance checklist\n1-year update service',
             False, False),
            # 咨询服务
            ('双体系认证辅导（企业版）', 'Dual System Consulting (Enterprise)', 'dual-consulting',
             consulting_cat, 'consulting', 4980, 697,
             '1对1企业级双体系认证辅导，包含现场审核、文件编写、员工培训、模拟审核全流程。',
             'Enterprise-level 1-on-1 dual system certification consulting with on-site audit, documentation, training, and mock audit.',
             '现场风险评估\n文件体系编写\n全员安全培训\n模拟审核\n认证辅导',
             'On-site risk assessment\nDocumentation system\nStaff safety training\nMock audit\nCertification guidance',
             True, True),
            ('工厂风险评估服务', 'Factory Risk Assessment Service', 'factory-risk-assess',
             consulting_cat, 'consulting', 2980, 417,
             '专业安全专家现场评估工厂风险，输出详细的评估报告和整改建议。',
             'Professional on-site factory risk assessment with detailed report and rectification recommendations.',
             '现场勘查（1-3天）\n详细评估报告\n整改优先级排序\n跟进支持',
             'On-site inspection (1-3 days)\nDetailed assessment report\nRemediation prioritization\nFollow-up support',
             False, False),
            ('单次在线安全咨询', 'One-time Online Consultation', 'online-consult',
             consulting_cat, 'consulting', 399, 55,
             '60分钟在线一对一安全合规咨询，解答您的具体问题和困惑。',
             '60-minute 1-on-1 online safety compliance consultation.',
             '60分钟视频会议\n问题预先收集\n会议纪要\n后续邮件跟进',
             '60-minute video call\nPre-meeting question collection\nMeeting minutes\nEmail follow-up',
             False, False),
            # 自查工具
            ('100条安全自查清单', '100-Item Safety Checklist', 'safety-checklist-100',
             tool_cat, 'tool', 0, 0,
             '东南亚工厂安全合规自查清单（100条），免费下载。',
             'SE Asia factory safety compliance self-assessment checklist (100 items), free download.',
             '100条自查项目\n覆盖设备/消防/电气/化学品\n中英双语\n含评分标准',
             '100 self-check items\nEquipment/fire/electrical/chemicals\nBilingual\nWith scoring criteria',
             False, False),
            ('消防隐患排查清单', 'Fire Hazard Inspection Checklist', 'fire-checklist',
             tool_cat, 'tool', 99, 14,
             '工厂消防安全隐患排查专业清单，涵盖消防设施、逃生通道、灭火器材等。',
             'Professional factory fire safety hazard inspection checklist.',
             '消防设施检查\n逃生通道评估\n灭火器材配置\n应急照明检查',
             'Fire facility inspection\nEscape route assessment\nFire extinguisher allocation\nEmergency lighting check',
             False, False),
        ]
        for name_zh, name_en, slug, cat, ptype, price_cny, price_usd, desc_zh, desc_en, feat_zh, feat_en, featured, free in products:
            Product.objects.get_or_create(slug=slug, defaults={
                'name_zh': name_zh, 'name_en': name_en, 'category': cat,
                'product_type': ptype, 'price_cny': price_cny, 'price_usd': price_usd,
                'description_zh': desc_zh, 'description_en': desc_en,
                'features_zh': feat_zh, 'features_en': feat_en,
                'is_active': True, 'is_featured': featured, 'is_free': free,
                'stock': 999 if not free else 9999,
            })
        self.stdout.write(f'OK: {len(products)} Products')

        # 6. 博客分类
        blog_cats = [
            ('ISO认证', 'ISO Certification', 'iso'),
            ('法规解读', 'Regulation Guide', 'regulations'),
            ('安全管理', 'Safety Management', 'safety'),
            ('案例分析', 'Case Study', 'cases'),
        ]
        for name_zh, name_en, slug in blog_cats:
            PostCategory.objects.get_or_create(slug=slug, defaults={
                'name_zh': name_zh, 'name_en': name_en
            })
        self.stdout.write(f'OK: {len(blog_cats)} Blog categories')

        # 7. 博客标签
        tags = ['ISO 45001', 'ISO 14001', '东南亚', '非洲', '设备安全', '消防安全',
                '风险评估', '法规合规', '安全管理', '中资出海']
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
        self.stdout.write(f'OK: {len(tags)} Tags')

        # 8. 博客文章
        iso_cat = PostCategory.objects.get(slug='iso')
        reg_cat = PostCategory.objects.get(slug='regulations')
        safety_cat = PostCategory.objects.get(slug='safety')
        case_cat = PostCategory.objects.get(slug='cases')

        posts = [
            ('ISO 45001:2018 七大核心条款解读', 'ISO 45001:2018 Core Clauses Explained',
             iso_cat, 'featured',
             '全面解读ISO 45001:2018的七大核心条款，帮助企业理解标准要求并有效实施。',
             'Comprehensive explanation of the 7 core clauses of ISO 45001:2018.',
             'ISO 45001:2018于2018年3月发布，取代了OHSAS 18001。本文将详细解读其七大核心条款...',
             'Published'),
            ('ISO 14001环境管理体系实施指南', 'ISO 14001 EMS Implementation Guide',
             iso_cat, '',
             '从零开始实施ISO 14001环境管理体系的完整指南，包含步骤、工具和模板。',
             'Complete guide to implementing ISO 14001 EMS from scratch.',
             'ISO 14001环境管理体系是全球应用最广泛的环境管理标准...',
             'Published'),
            ('越南工厂安全管理法规概览', 'Overview of Vietnam Factory Safety Regulations',
             reg_cat, '',
             '中国企业在越南建厂需要了解的安全法规要点，包括QSV/TCLL等核心法规。',
             'Key safety regulations Chinese companies need to know when setting up factories in Vietnam.',
             '越南是中国企业出海东南亚的首选目的地之一...',
             'Published'),
            ('印尼安全法规：企业必知的10个要点', 'Indonesia Safety Regulations: 10 Must-Know Points',
             reg_cat, '',
             '解读印尼工厂安全管理的核心法规要求，包括K3法规、工厂法等。',
             'Understanding core regulatory requirements for factory safety in Indonesia.',
             '印度尼西亚作为东南亚最大的经济体...',
             'Published'),
            ('设备风险评估方法论与实操', 'Equipment Risk Assessment Methodology',
             safety_cat, '',
             '系统介绍设备风险评估的方法论，包括LEC法、故障树分析法等常用工具。',
             'Systematic introduction to equipment risk assessment methodologies.',
             '设备风险评估是工厂安全管理的核心工作之一...',
             'Published'),
            ('消防安全设计：从法规到实践', 'Fire Safety Design: From Regulations to Practice',
             safety_cat, '',
             '如何将消防法规要求转化为实际的消防安全设计方案。',
             'How to translate fire safety regulation requirements into practical design solutions.',
             '消防安全设计是工厂建设中最容易被忽视却又最关键的环节...',
             'Published'),
            ('案例：某越南中资工厂ISO认证经验', 'Case Study: ISO Certification at a Chinese Factory in Vietnam',
             case_cat, 'featured',
             '分享某越南中资工厂从零开始通过ISO 45001认证的完整经验。',
             'Sharing the complete experience of a Chinese factory in Vietnam achieving ISO 45001 certification.',
             '2024年，我们帮助一家位于越南平阳省的中资电子厂...',
             'Published'),
            ('中资出海企业安全合规趋势 2025', 'Safety Compliance Trends for Chinese Enterprises Going Global 2025',
             case_cat, '',
             '2025年中资出海企业安全合规的最新趋势和挑战分析。',
             'Analysis of latest trends and challenges in safety compliance for Chinese enterprises expanding overseas in 2025.',
             '随着越来越多的中国企业将生产基地转移到东南亚和非洲...',
             'Published'),
        ]
        for title_zh, title_en, cat, featured, excerpt_zh, excerpt_en, content_zh, status in posts:
            slug = title_en.lower().replace(' ', '-').replace(':', '').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('+', '')[:80]
            Post.objects.get_or_create(slug=slug, defaults={
                'title_zh': title_zh, 'title_en': title_en, 'category': cat,
                'excerpt_zh': excerpt_zh, 'excerpt_en': excerpt_en,
                'content_zh': content_zh, 'content_en': content_zh,
                'status': status, 'is_featured': bool(featured),
                'author': 'YigeWorks',
            })
        self.stdout.write(f'OK: {len(posts)} Blog posts')

        self.stdout.write(self.style.SUCCESS('\n全部初始数据创建完成！'))
