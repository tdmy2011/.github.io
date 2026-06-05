# -*- coding: utf-8 -*-
"""
Marketing App -- Django Signals
自动触发邮件 Drip Campaign

触发关系:
  Lead 创建 → send_welcome_email (5 分钟后)
  Lead 更新 stage=converted → 更新关联漏斗
  ContentEngagement 创建 (is_qualified=True) → send_report_email
  Order 创建 → 更新 Lead stage 为 converted
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger("apps.marketing")


@receiver(post_save, sender="marketing.Lead")
def on_lead_created(sender, instance, created, **kwargs):
    """
    新线索创建 → 5 分钟后发送欢迎邮件
    CAN-SPAM / GDPR: 仅在 consent_marketing=True 时发送
    """
    if created:
        from .tasks import send_welcome_email

        # 设置同意时间戳
        if instance.consent_marketing and not instance.consent_timestamp:
            sender.objects.filter(pk=instance.pk).update(
                consent_timestamp=timezone.now()
            )

        # 5 分钟延迟，让用户完成页面交互
        send_welcome_email.apply_async(
            args=[instance.id],
            countdown=5 * 60,  # 5 分钟
        )
        logger.info(f"[Signal] 新线索 {instance.email} → 欢迎邮件已排队 (5 分钟后)")


@receiver(post_save, sender="marketing.ContentEngagement")
def on_engagement_qualified(sender, instance, created, **kwargs):
    """
    内容互动变为有效 (is_qualified=True) → 发送行业报告邮件
    """
    if created and instance.is_qualified:
        # 检查访客是否已有 Lead
        lead = getattr(instance.visitor, "lead", None)
        if lead:
            from .tasks import send_report_email
            send_report_email.apply_async(
                args=[lead.id, instance.content_title],
                countdown=0,  # 立即发送
            )
            logger.info(f"[Signal] L2 互动 → 报告邮件已排队 ({lead.email})")


@receiver(post_save, sender="marketing.Order")
def on_order_created(sender, instance, created, **kwargs):
    """
    L5 订单创建 → 更新关联 Lead 阶段为 converted
    """
    if created and instance.lead:
        instance.lead.stage = "converted"
        instance.lead.save(update_fields=["stage"])
        logger.info(f"[Signal] 订单 #{instance.order_number} → Lead {instance.lead.email} 已转化")
