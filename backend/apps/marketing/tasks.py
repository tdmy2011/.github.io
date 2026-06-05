# -*- coding: utf-8 -*-
"""
Marketing App -- Celery 异步任务
Drip Campaign 邮件触达 + 漏斗引擎 + Geo 报告

任务清单:
  process_visitor           - L1 访客异步入库
  apply_auto_rules          - 自动营销规则引擎
  send_drip_email           - 通用 Drip 邮件发送
  send_welcome_email        - L3 新线索欢迎邮件 (立即)
  send_report_email         - L3 行业报告邮件 (立即)
  send_abandoned_cart       - L4 弃单挽回邮件 (24h 后)
  send_reengagement_email   - 30天未活跃复购激活
  check_abandoned_intents   - 定时检查弃单 (Beat 调度)
  daily_geo_report          - 每日 Geo 数据聚合
"""

import logging
from datetime import timedelta
from urllib.parse import urlparse

from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, Context

logger = logging.getLogger("apps.marketing")

# 退订链接 (生产环境需要替换为真实 URL)
UNSUBSCRIBE_BASE_URL = getattr(settings, "UNSUBSCRIBE_BASE_URL",
                                "https://yigeworks.com/unsubscribe/")


# ============================================================
# 辅助函数
# ============================================================

def _render_template(template_str: str, context: dict) -> str:
    """渲染 Django 模板字符串"""
    try:
        tpl = Template(template_str)
        return tpl.render(Context(context))
    except Exception:
        return template_str.format(**context)


def _add_gdpr_footer(body: str, lead_email: str) -> str:
    """
    GDPR / CAN-SPAM 合规：在邮件底部附加退订链接
    所有营销邮件必须包含此内容
    """
    unsubscribe_url = f"{UNSUBSCRIBE_BASE_URL}?email={lead_email}"
    footer = f"""

---
YigeWorks | Global HSE Compliance Consulting
www.yigeworks.com | noreply@yigeworks.com

To unsubscribe from marketing emails, click here:
{unsubscribe_url}

This email was sent to {lead_email} because you subscribed to YigeWorks updates.
YigeWorks complies with GDPR, CAN-SPAM, and applicable local data protection laws.
"""
    return body + footer


def _send_gdpr_compliant_email(lead, subject: str, body: str, drip_trigger: str = "") -> bool:
    """
    统一邮件发送入口
    - 检查 consent_marketing 和 unsubscribed
    - 自动附加退订链接 (GDPR / CAN-SPAM)
    - 记录 EmailLog
    """
    from .models import EmailLog, EmailDrip

    if not lead.can_send_email():
        logger.info(f"[邮件跳过] {lead.email} — 未授权或已退订")
        return False

    # 附加 GDPR 退订页脚
    body_with_footer = _add_gdpr_footer(body, lead.email)

    try:
        send_mail(
            subject=subject,
            message=body_with_footer,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead.email],
            fail_silently=False,
        )
        status = "sent"
    except Exception as e:
        logger.error(f"[邮件失败] {lead.email} — {e}")
        # 记录失败日志
        EmailLog.objects.create(
            lead=lead,
            subject=subject,
            status="failed",
            error_message=str(e),
        )
        return False

    # 记录成功日志
    drip = None
    if drip_trigger:
        drip = EmailDrip.objects.filter(trigger=drip_trigger, is_active=True).first()

    EmailLog.objects.create(
        lead=lead,
        drip=drip,
        subject=subject,
        status="sent",
    )
    logger.info(f"[邮件成功] {lead.email} — {subject}")
    return True


# ============================================================
# L1: 访客入库
# ============================================================

@shared_task(name="marketing.process_visitor")
def process_visitor(ip_address, country_code, city, device_type, referrer,
                    landing_page, utm_params=None, user_agent=""):
    """
    L1 — 异步处理访客日志入库，避免阻塞 HTTP 响应
    """
    from .models import VisitorLog, Campaign

    utm_params = utm_params or {}
    utm_source = utm_params.get("utm_source", "")
    utm_medium = utm_params.get("utm_medium", "")
    utm_campaign = utm_params.get("utm_campaign", "")

    # 解析 referrer 域名
    ref_domain = ""
    if referrer:
        try:
            ref_domain = urlparse(referrer).netloc
        except Exception:
            pass

    # 匹配关联活动
    campaign = None
    if utm_campaign:
        campaign = Campaign.objects.filter(utm_campaign=utm_campaign, status="active").first()

    visitor = VisitorLog.objects.create(
        ip_address=ip_address,
        country=country_code,
        city=city or "",
        device_type=device_type or "other",
        referrer=referrer or "",
        referrer_domain=ref_domain,
        landing_page=landing_page or "",
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        campaign=campaign,
    )

    # 触发自动规则引擎
    apply_auto_rules.delay(visitor.id)
    return visitor.id


# ============================================================
# 自动规则引擎
# ============================================================

@shared_task(name="marketing.apply_auto_rules")
def apply_auto_rules(visitor_id):
    """
    匹配活跃活动规则 → 触发自动邮件 / 延迟 Drip
    规则逻辑: 国家匹配 + 页面匹配 → 延迟发送欢迎邮件
    """
    from .models import VisitorLog, Campaign

    try:
        visitor = VisitorLog.objects.get(id=visitor_id)
    except VisitorLog.DoesNotExist:
        return

    active_campaigns = Campaign.objects.filter(status="active", auto_rule_enabled=True)

    for campaign in active_campaigns:
        match = True

        if campaign.target_countries:
            code = visitor.country.code if visitor.country else ""
            if code not in campaign.target_countries:
                match = False

        if campaign.target_page_pattern and visitor.landing_page:
            if campaign.target_page_pattern not in visitor.landing_page:
                match = False

        if match:
            send_drip_email.apply_async(
                args=[visitor_id, campaign.id],
                countdown=campaign.delay_minutes * 60,
            )


# ============================================================
# 通用 Drip Email
# ============================================================

@shared_task(name="marketing.send_drip_email")
def send_drip_email(visitor_id, campaign_id):
    """
    通用 Drip Email — 由自动规则引擎触发
    需要访客已有关联 Lead 且授权营销
    """
    from .models import VisitorLog, Campaign

    try:
        visitor = VisitorLog.objects.get(id=visitor_id)
        campaign = Campaign.objects.get(id=campaign_id)
    except (VisitorLog.DoesNotExist, Campaign.DoesNotExist):
        return False

    lead = getattr(visitor, "lead", None)
    if not lead:
        logger.debug(f"[Drip 跳过] visitor={visitor_id} 尚无关联 Lead")
        return False

    subject = f"[{campaign.name}] Welcome from YigeWorks"
    body = campaign.welcome_email_template or f"""
Hi {lead.name or lead.email},

Thank you for your interest in YigeWorks HSE & ISO compliance solutions.

As a professional serving {lead.country.name if lead.country else 'your region'}, 
you may face unique compliance challenges. We're here to help.

Learn more: https://yigeworks.com/course.html

Best regards,
The YigeWorks Team
"""
    return _send_gdpr_compliant_email(lead, subject, body, "visitor_welcome")


# ============================================================
# L3: 线索欢迎邮件 (Signal 触发)
# ============================================================

@shared_task(name="marketing.send_welcome_email")
def send_welcome_email(lead_id: int):
    """
    L3 — 新线索欢迎邮件 (创建线索后 5 分钟自动触发，via signals.py)
    符合 CAN-SPAM：包含退订链接
    """
    from .models import Lead

    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return False

    if lead.email_sent_welcome:
        return False  # 防止重复发送

    country_name = lead.country.name if lead.country else "your region"
    product_name = lead.interested_product or "ISO 45001/14001 Dual System Program"

    subject = "Welcome to YigeWorks — Your HSE Compliance Partner"
    body = f"""Hi {lead.name or "there"},

Welcome to YigeWorks!

Thank you for reaching out. As a professional in {country_name}, you're navigating 
some of the most challenging HSE and environmental compliance requirements for 
Chinese overseas enterprises.

Here's what we can help you with:
✅ ISO 45001 (Occupational Health & Safety)
✅ ISO 14001 (Environmental Management)
✅ Dual System Integration (the most cost-effective path to compliance)

You showed interest in: {product_name}

👉 Explore our courses: https://yigeworks.com/course.html
👉 Download free compliance guide: https://yigeworks.com/东南亚四国法规对照表.html

We'll be in touch shortly.

Best regards,
YigeWorks HSE Consulting Team
"""

    success = _send_gdpr_compliant_email(lead, subject, body, "lead_welcome")
    if success:
        lead.email_sent_welcome = True
        lead.save(update_fields=["email_sent_welcome"])
    return success


# ============================================================
# L3: 行业报告邮件
# ============================================================

@shared_task(name="marketing.send_report_email")
def send_report_email(lead_id: int, report_name: str = ""):
    """
    L3 — 用户下载智库报告后发送完整报告 + Case Study
    """
    from .models import Lead

    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return False

    if lead.email_sent_report:
        return False

    report_name = report_name or "Southeast Asia HSE Compliance Guide"
    subject = f"Your Report: {report_name} — YigeWorks"
    body = f"""Hi {lead.name or "there"},

Your requested report is ready: "{report_name}"

📥 Download link: https://yigeworks.com/reports/{report_name.replace(' ', '_').lower()}.pdf

What's inside:
• Regulatory comparison: Vietnam, Thailand, Indonesia, Nigeria
• ISO 45001 + 14001 dual system integration roadmap
• 100-point safety compliance checklist for overseas factories
• Common audit failure points and solutions

---
📌 CASE STUDY: How a Chinese manufacturing company achieved dual certification in 6 months
Read here → https://yigeworks.com/thinktank/case-study-1.html

Need help with your specific project? Reply to this email for a free 30-minute consultation.

Best regards,
YigeWorks HSE Consulting Team
"""

    success = _send_gdpr_compliant_email(lead, subject, body, "report_download")
    if success:
        lead.email_sent_report = True
        lead.save(update_fields=["email_sent_report"])
    return success


# ============================================================
# L4: 弃单挽回邮件
# ============================================================

@shared_task(name="marketing.send_abandoned_cart")
def send_abandoned_cart(intent_id: int):
    """
    L4 — 弃单挽回邮件 (结账未完成 24h 后触发)
    赠送限时折扣码
    """
    from .models import IntentEvent

    try:
        intent = IntentEvent.objects.get(id=intent_id)
    except IntentEvent.DoesNotExist:
        return False

    if intent.is_completed:
        return False  # 已完成，无需挽回

    lead = intent.lead
    if not lead:
        return False

    if lead.email_sent_discount:
        return False

    discount_code = f"BACK{lead.id:04d}"
    product_name = intent.product_name or "our course"

    subject = f"Still interested in {product_name}? Here's a 15% discount 🎁"
    body = f"""Hi {lead.name or "there"},

We noticed you were checking out "{product_name}" but didn't complete your purchase.

We'd love to help you get started. Here's a special offer just for you:

🎁 Use code: {discount_code}
💰 Get 15% OFF your first purchase
⏰ Valid for 48 hours only

👉 Complete your order: https://yigeworks.com/course.html

Why YigeWorks?
• Expert-led ISO 45001 + 14001 training
• Specifically designed for Chinese overseas enterprises
• Includes 15 ready-to-use procedure document templates
• 30-day money-back guarantee

If you have any questions, reply to this email — we respond within 24 hours.

Best regards,
YigeWorks HSE Consulting Team
"""

    success = _send_gdpr_compliant_email(lead, subject, body, "abandoned_cart")
    if success:
        lead.email_sent_discount = True
        lead.save(update_fields=["email_sent_discount"])
    return success


# ============================================================
# 复购激活: 30天未活跃
# ============================================================

@shared_task(name="marketing.send_reengagement_email")
def send_reengagement_email(lead_id: int):
    """
    30天未活跃 → 复购激活邮件 (新品/新内容通知)
    """
    from .models import Lead

    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return False

    subject = "New ISO content just for you 🌏 — YigeWorks"
    body = f"""Hi {lead.name or "there"},

It's been a while! We've added new content we think you'll find valuable:

🆕 NEW: ISO 14001:2015 Environmental Aspects Identification Workshop
🆕 NEW: ASEAN Labour Law & ISO 45001 Integration Guide (2026 Edition)
🆕 UPDATED: 100-Point Factory Safety Checklist — now with Vietnam & Nigeria editions

👉 Check out what's new: https://yigeworks.com/course.html

As one of our valued subscribers, you get early access to our new content library.
Over 50 procedure document templates now available for immediate download.

Click here to explore → https://yigeworks.com

Best regards,
YigeWorks HSE Consulting Team
"""

    return _send_gdpr_compliant_email(lead, subject, body, "reengagement")


# ============================================================
# Beat 调度任务: 弃单检查
# ============================================================

@shared_task(name="marketing.check_abandoned_intents")
def check_abandoned_intents():
    """
    每小时由 Celery Beat 调用
    检查 L4 弃单 → 触发挽回邮件
    """
    from .models import IntentEvent

    cutoff = timezone.now() - timedelta(hours=24)
    abandoned = IntentEvent.objects.filter(
        is_completed=False,
        created_at__lte=cutoff,
        lead__isnull=False,
        lead__email_sent_discount=False,
    )

    count = 0
    for intent in abandoned:
        send_abandoned_cart.delay(intent.id)
        count += 1

    logger.info(f"[弃单检查] 触发了 {count} 封挽回邮件")
    return count


# ============================================================
# Beat 调度任务: 30天复购激活
# ============================================================

@shared_task(name="marketing.check_reengagement")
def check_reengagement():
    """
    每天由 Celery Beat 调用
    检查 30 天未活跃线索 → 触发复购激活邮件
    """
    from .models import Lead

    cutoff = timezone.now() - timedelta(days=30)
    inactive_leads = Lead.objects.filter(
        updated_at__lte=cutoff,
        unsubscribed=False,
        consent_marketing=True,
        stage__in=["new", "contacted"],
    )

    count = 0
    for lead in inactive_leads:
        send_reengagement_email.delay(lead.id)
        count += 1

    logger.info(f"[复购激活] 触发了 {count} 封复购邮件")
    return count


# ============================================================
# Beat 调度任务: 每日 Geo 报告
# ============================================================

@shared_task(name="marketing.daily_geo_report")
def daily_geo_report():
    """
    每日 Geo 数据聚合报告
    统计各国家访客数、新线索数、转化率、漏斗健康度
    """
    from .models import VisitorLog, Lead, ContentEngagement, IntentEvent, Order
    from django.db.models import Count, Sum

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # 各层漏斗数量
    l1 = VisitorLog.objects.filter(first_visited__date=yesterday).count()
    l2 = ContentEngagement.objects.filter(created_at__date=yesterday, is_qualified=True).count()
    l3 = Lead.objects.filter(created_at__date=yesterday).count()
    l4 = IntentEvent.objects.filter(created_at__date=yesterday).count()
    l5 = Order.objects.filter(paid_at__date=yesterday).count()
    revenue = Order.objects.filter(paid_at__date=yesterday).aggregate(
        total=Sum("amount"))["total"] or 0

    # 国家访客统计
    visitors_by_country = (
        VisitorLog.objects.filter(first_visited__date=yesterday)
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    report = {
        "date": str(yesterday),
        "funnel": {
            "L1_visitors": l1,
            "L2_engaged": l2,
            "L3_leads": l3,
            "L4_intents": l4,
            "L5_orders": l5,
        },
        "revenue_usd": float(revenue),
        "conversion_l1_to_l5": f"{round(l5 / l1 * 100, 2)}%" if l1 else "0%",
        "top_countries": [
            {"country": v["country"], "visitors": v["count"]}
            for v in visitors_by_country
        ],
    }

    logger.info(f"[每日 Geo 报告] {report}")
    return report
