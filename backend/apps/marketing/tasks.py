# -*- coding: utf-8 -*-
"""
Marketing App -- Celery 异步任务
- 自动营销规则引擎
- Geo 数据聚合
- 邮件发送
"""

import hashlib
import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(name="marketing.process_visitor")
def process_visitor(ip_address, country_code, city, device_type, referrer, landing_page,
                    utm_params=None, user_agent=""):
    """
    异步处理访客日志入库，避免阻塞 HTTP 响应
    由前端 API 或中间件调用
    """
    from .models import VisitorLog, Campaign

    utm_source = utm_params.get("utm_source", "") if utm_params else ""
    utm_medium = utm_params.get("utm_medium", "") if utm_params else ""
    utm_campaign = utm_params.get("utm_campaign", "") if utm_params else ""

    # IP 哈希 (GDPR)
    ip_hash = hashlib.sha256(ip_address.encode()).hexdigest() if ip_address else ""

    # 解析 referrer 域名
    from urllib.parse import urlparse
    ref_domain = ""
    if referrer:
        try:
            ref_domain = urlparse(referrer).netloc
        except Exception:
            pass

    # 匹配关联活动
    campaign = None
    if utm_campaign:
        campaign = Campaign.objects.filter(
            utm_campaign=utm_campaign, status="active"
        ).first()

    visitor = VisitorLog.objects.create(
        ip_address=ip_address,
        ip_hash=ip_hash,
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

    # 自动营销规则引擎
    apply_auto_rules.delay(visitor.id)

    return visitor.id


@shared_task(name="marketing.apply_auto_rules")
def apply_auto_rules(visitor_id):
    """
    自动规则引擎：匹配活跃活动规则，触发自动动作
    """
    from .models import VisitorLog, Campaign

    try:
        visitor = VisitorLog.objects.get(id=visitor_id)
    except VisitorLog.DoesNotExist:
        return

    # 查询所有启用自动规则的活动
    active_campaigns = Campaign.objects.filter(
        status="active", auto_rule_enabled=True
    )

    for campaign in active_campaigns:
        match = True

        # 国家匹配
        if campaign.target_countries:
            country_code = visitor.country.code if visitor.country else ""
            if country_code not in campaign.target_countries:
                match = False

        # 页面匹配
        if campaign.target_page_pattern and visitor.landing_page:
            if campaign.target_page_pattern not in visitor.landing_page:
                match = False

        if match:
            # 延迟执行欢迎邮件
            send_welcome_email.apply_async(
                args=[visitor.id, campaign.id],
                countdown=campaign.delay_minutes * 60,
            )


@shared_task(name="marketing.send_welcome_email")
def send_welcome_email(visitor_id, campaign_id):
    """
    发送自动化欢迎邮件
    TODO: 对接 SendGrid / Mailgun / SES API
    """
    from .models import VisitorLog, Campaign, Lead

    try:
        visitor = VisitorLog.objects.get(id=visitor_id)
        campaign = Campaign.objects.get(id=campaign_id)
    except (VisitorLog.DoesNotExist, Campaign.DoesNotExist):
        return

    # 检查是否已有 Lead
    lead = Lead.objects.filter(visitor=visitor).first()

    if campaign.welcome_email_template:
        # 发送邮件逻辑 (placeholder)
        logger.info(
            f"[营销自动化] 活动={campaign.name} → 访客={visitor.country.name} "
            f"已触发欢迎邮件 (延迟 {campaign.delay_minutes} 分钟)"
        )
        # TODO: 对接 SendGrid / Mailgun API
        # send_email(to=lead.email or "unknown", template=campaign.welcome_email_template)

    return True


@shared_task(name="marketing.daily_geo_report")
def daily_geo_report():
    """
    每日 Geo 数据聚合报告
    统计各国家访客数、新线索数、转化率
    """
    from .models import VisitorLog, Lead
    from django.db.models import Count

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # 国家访客统计
    visitors_by_country = (
        VisitorLog.objects.filter(first_visited__date=yesterday)
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # 新线索统计
    new_leads = Lead.objects.filter(created_at__date=yesterday).count()

    report = {
        "date": str(yesterday),
        "total_visitors": sum(v["count"] for v in visitors_by_country),
        "new_leads": new_leads,
        "by_country": [
            {"country": v["country"], "visitors": v["count"]}
            for v in visitors_by_country[:10]
        ],
    }

    logger.info(f"[每日 Geo 报告] {report}")
    return report
