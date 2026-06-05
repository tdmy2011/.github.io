# -*- coding: utf-8 -*-
"""
YigeWorks SaaS Platform -- Marketing App Models
Geo 全球获客营销 · 5 层转化漏斗 + 邮件触达 + GDPR 合规

Funnel 层级:
  L1 全球访客  → VisitorLog       (IP 命中海外节点)
  L2 内容兴趣  → ContentEngagement (浏览智库 / 停留 > 60s)
  L3 线索捕获  → Lead             (下载报告 / 订阅 / 留邮)
  L4 商业意图  → IntentEvent      (查看 Pricing / 加购)
  L5 付费客户  → Order            (支付成功)

依赖: django-countries, GeoIP2, Celery
"""

import hashlib
from django.db import models
from django.utils import timezone as tz
from django_countries.fields import CountryField


# ============================================================
# 常量
# ============================================================

GDPR_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE", "GB", "IS", "LI", "NO", "CH",
}


def hash_ip(ip_address: str) -> str:
    """SHA-256 哈希 IP，满足 GDPR 伪匿名化要求"""
    if not ip_address:
        return ""
    return hashlib.sha256(ip_address.encode()).hexdigest()


# ============================================================
# Campaign (推广活动 - 增强版)
# ============================================================

class Campaign(models.Model):
    """推广活动 — UTM 追踪 + 自动化营销规则引擎"""
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("active", "运行中"),
        ("paused", "已暂停"),
        ("ended", "已结束"),
    ]

    name = models.CharField("活动名称", max_length=200)
    slug = models.SlugField("URL 标识", max_length=80, unique=True)
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default="draft")
    description = models.TextField("活动描述", blank=True)

    # --- UTM 自动化 ---
    utm_source = models.CharField("UTM Source", max_length=120, blank=True)
    utm_medium = models.CharField("UTM Medium", max_length=120, blank=True)
    utm_campaign = models.CharField("UTM Campaign", max_length=120, blank=True)

    # --- 自动化规则 ---
    auto_rule_enabled = models.BooleanField("启用自动规则", default=False)
    target_countries = models.JSONField("目标国家", default=list, blank=True,
        help_text="例如: ['US', 'GB', 'VN', 'TH']")
    target_page_pattern = models.CharField("目标页面匹配", max_length=200, blank=True,
        help_text="例如: /pricing/ 匹配所有定价页访问")
    delay_minutes = models.PositiveIntegerField("延迟分钟数", default=10)
    welcome_email_template = models.TextField("欢迎邮件模板", blank=True)

    # --- 预算 ---
    budget = models.DecimalField("预算 (USD)", max_digits=10, decimal_places=2, default=0)
    spent = models.DecimalField("已花费 (USD)", max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "推广活动"
        verbose_name_plural = "推广活动"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def roi(self):
        """简单 ROI: (线索数 * 50 - 花费) / 花费 * 100"""
        if self.spent == 0:
            return 0
        leads = self.leads.count()
        return round((leads * 50 - float(self.spent)) / float(self.spent) * 100, 1)

    @property
    def conversion_rate(self):
        """转化率: L5 订单 / L1 访客"""
        visitors = self.visitors.count()
        if visitors == 0:
            return 0
        orders = self.orders.count()
        return round(orders / visitors * 100, 2)


# ============================================================
# L1: VisitorLog (全球访客)
# ============================================================

class VisitorLog(models.Model):
    """L1 — 全球访客日志 (IP 命中海外节点)"""
    DEVICE_CHOICES = [
        ("mobile", "手机"),
        ("tablet", "平板"),
        ("desktop", "桌面"),
        ("other", "其他"),
    ]

    # 漏斗标记
    funnel_stage = models.CharField("漏斗层级", max_length=2, default="L1", editable=False)

    # 地理位置
    ip_address = models.GenericIPAddressField("IP 地址", null=True, blank=True)
    ip_hash = models.CharField("IP 哈希 (GDPR)", max_length=64, blank=True, db_index=True,
        help_text="SHA-256 哈希后的 IP，满足 GDPR 要求")
    country = CountryField("国家/地区", blank=True, blank_label="(未知)")
    city = models.CharField("城市", max_length=100, blank=True)
    region = models.CharField("省/州", max_length=100, blank=True)
    timezone_name = models.CharField("时区", max_length=50, blank=True)

    # 设备信息
    device_type = models.CharField("设备类型", max_length=20, choices=DEVICE_CHOICES, default="other")
    browser = models.CharField("浏览器", max_length=100, blank=True)
    os = models.CharField("操作系统", max_length=100, blank=True)

    # 流量来源
    referrer = models.URLField("来源链接", max_length=500, blank=True)
    referrer_domain = models.CharField("来源域名", max_length=200, blank=True)
    landing_page = models.CharField("着陆页", max_length=500, blank=True)

    # UTM 参数
    utm_source = models.CharField("UTM Source", max_length=200, blank=True)
    utm_medium = models.CharField("UTM Medium", max_length=200, blank=True)
    utm_campaign = models.CharField("UTM Campaign", max_length=200, blank=True)
    utm_term = models.CharField("UTM Term", max_length=200, blank=True)
    utm_content = models.CharField("UTM Content", max_length=200, blank=True)

    # 关联
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="visitors", verbose_name="关联活动")

    # GDPR / 合规
    is_gdpr_region = models.BooleanField("GDPR 地区", default=False,
        help_text="是否来自 EU/EEA 或英国")
    consent_given = models.BooleanField("已授权追踪", default=False)

    # 时间统计
    first_visited = models.DateTimeField("首次访问", default=tz.now)
    last_seen = models.DateTimeField("最近活跃", auto_now=True)
    visit_count = models.PositiveIntegerField("访问次数", default=1)

    class Meta:
        verbose_name = "L1 访客日志"
        verbose_name_plural = "L1 访客日志"
        ordering = ["-first_visited"]
        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["ip_hash"]),
            models.Index(fields=["first_visited"]),
            models.Index(fields=["funnel_stage"]),
        ]

    def __str__(self):
        return f"[L1] {self.country.name or 'Unknown'} - {self.ip_hash[:8] if self.ip_hash else 'NoIP'} - {self.first_visited.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if self.ip_address and not self.ip_hash:
            self.ip_hash = hash_ip(self.ip_address)
        if self.country and self.country.code in GDPR_COUNTRIES:
            self.is_gdpr_region = True
        super().save(*args, **kwargs)


# ============================================================
# L2: ContentEngagement (内容兴趣)
# ============================================================

class ContentEngagement(models.Model):
    """L2 — 内容兴趣 (浏览智库文章 / 停留 > 60s)"""
    ENGAGEMENT_TYPE = [
        ("page_view", "页面浏览"),
        ("article_read", "文章阅读"),
        ("video_watch", "视频观看"),
        ("download", "资料下载"),
        ("scroll_80", "滚动至80%"),
    ]

    visitor = models.ForeignKey(VisitorLog, on_delete=models.CASCADE,
        related_name="engagements", verbose_name="关联访客")

    funnel_stage = models.CharField("漏斗层级", max_length=2, default="L2", editable=False)
    engagement_type = models.CharField("互动类型", max_length=20, choices=ENGAGEMENT_TYPE)
    content_url = models.CharField("内容 URL", max_length=500, blank=True)
    content_title = models.CharField("内容标题", max_length=300, blank=True)

    # 停留统计
    duration_seconds = models.PositiveIntegerField("停留时长(秒)", default=0,
        help_text="停留超过 60s 视为有效兴趣")
    is_qualified = models.BooleanField("有效互动", default=False,
        help_text="停留超过 60s 或下载/阅读完成标记为 True")

    # 设备 & 来源
    device_type = models.CharField("设备", max_length=20, blank=True)
    country = CountryField("国家/地区", blank=True)

    created_at = models.DateTimeField("互动时间", auto_now_add=True)

    class Meta:
        verbose_name = "L2 内容互动"
        verbose_name_plural = "L2 内容互动"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["visitor", "engagement_type"]),
            models.Index(fields=["is_qualified"]),
        ]

    def __str__(self):
        return f"[L2] {self.visitor.ip_hash[:8]} - {self.get_engagement_type_display()} - {self.content_title[:40]}"

    def save(self, *args, **kwargs):
        # 自动标记有效互动
        if self.duration_seconds >= 60 or self.engagement_type in ("download", "video_watch"):
            self.is_qualified = True
        super().save(*args, **kwargs)


# ============================================================
# L3: Lead (线索捕获 - 增强版)
# ============================================================

class Lead(models.Model):
    """L3 — 营销线索 (下载报告 / 订阅 / 留邮)"""
    STAGE_CHOICES = [
        ("new", "新线索"),
        ("contacted", "已联系"),
        ("qualified", "已确认"),
        ("converted", "已转化"),
        ("closed", "已关闭"),
    ]

    SOURCE_CHOICES = [
        ("website", "官网"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
        ("facebook", "Facebook"),
        ("referral", "推荐"),
        ("event", "线下活动"),
        ("ad", "付费广告"),
        ("organic", "自然搜索"),
    ]

    # 漏斗标记
    funnel_stage = models.CharField("漏斗层级", max_length=2, default="L3", editable=False)

    email = models.EmailField("邮箱", unique=True)
    name = models.CharField("姓名", max_length=200, blank=True)
    company = models.CharField("公司", max_length=200, blank=True)
    job_title = models.CharField("职位", max_length=200, blank=True)

    country = CountryField("国家/地区", blank=True)
    phone = models.CharField("电话", max_length=30, blank=True)

    source = models.CharField("来源渠道", max_length=20, choices=SOURCE_CHOICES, default="website")
    source_page = models.CharField("来源页面", max_length=200, blank=True,
        help_text="捕获线索的具体页面 URL")
    stage = models.CharField("阶段", max_length=20, choices=STAGE_CHOICES, default="new")

    # 关联
    visitor = models.OneToOneField(VisitorLog, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="lead", verbose_name="关联访客")
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leads", verbose_name="来源活动")

    interested_product = models.CharField("感兴趣产品", max_length=200, blank=True)

    # 邮件触达状态
    email_sent_welcome = models.BooleanField("已发欢迎邮件", default=False)
    email_sent_report = models.BooleanField("已发行业报告", default=False)
    email_sent_discount = models.BooleanField("已发折扣", default=False)

    # GDPR 合规
    consent_marketing = models.BooleanField("同意营销邮件", default=False,
        help_text="用户明确勾选的营销同意")
    consent_timestamp = models.DateTimeField("同意时间", null=True, blank=True)
    unsubscribed = models.BooleanField("已退订", default=False)
    unsubscribed_at = models.DateTimeField("退订时间", null=True, blank=True)

    notes = models.TextField("备注", blank=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    contacted_at = models.DateTimeField("联系时间", null=True, blank=True)

    class Meta:
        verbose_name = "L3 营销线索"
        verbose_name_plural = "L3 营销线索"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stage"]),
            models.Index(fields=["country"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return f"[L3] {self.email} - {self.get_stage_display()}"

    def can_send_email(self):
        """检查是否允许发送营销邮件 (GDPR / CAN-SPAM)"""
        return self.consent_marketing and not self.unsubscribed

    def unsubscribe(self):
        """退订处理"""
        self.unsubscribed = True
        self.unsubscribed_at = tz.now()
        self.save(update_fields=["unsubscribed", "unsubscribed_at"])


# ============================================================
# L4: IntentEvent (商业意图)
# ============================================================

class IntentEvent(models.Model):
    """L4 — 商业意图 (查看 Pricing / 加购 / 试用申请)"""
    INTENT_TYPE = [
        ("pricing_view", "查看定价页"),
        ("add_to_cart", "加入购物车"),
        ("checkout_start", "开始结账"),
        ("trial_request", "申请试用"),
        ("consultation", "预约咨询"),
        ("demo_request", "申请演示"),
    ]

    visitor = models.ForeignKey(VisitorLog, on_delete=models.CASCADE,
        related_name="intents", verbose_name="关联访客")
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="intents", verbose_name="关联线索")
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="intents", verbose_name="来源活动")

    funnel_stage = models.CharField("漏斗层级", max_length=2, default="L4", editable=False)
    intent_type = models.CharField("意图类型", max_length=20, choices=INTENT_TYPE)
    product_name = models.CharField("目标产品", max_length=200, blank=True)
    product_price = models.DecimalField("产品价格", max_digits=8, decimal_places=2, default=0)

    # 购物车数据
    cart_items = models.JSONField("购物车内容", default=list, blank=True)

    # 是否完成
    is_completed = models.BooleanField("已完成操作", default=False)
    completed_at = models.DateTimeField("完成时间", null=True, blank=True)

    country = CountryField("国家/地区", blank=True)
    created_at = models.DateTimeField("触发时间", auto_now_add=True)

    class Meta:
        verbose_name = "L4 商业意图"
        verbose_name_plural = "L4 商业意图"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["intent_type"]),
            models.Index(fields=["is_completed"]),
        ]

    def __str__(self):
        return f"[L4] {self.get_intent_type_display()} - {self.product_name or 'N/A'}"

    @property
    def is_abandoned(self):
        """是否为弃单：创建 24h 后未完成"""
        if self.is_completed:
            return False
        return (tz.now() - self.created_at).total_seconds() > 86400


# ============================================================
# L5: Order (付费客户)
# ============================================================

class Order(models.Model):
    """L5 — 付费订单 (支付成功)"""
    PAYMENT_METHOD = [
        ("paypal", "PayPal"),
        ("stripe", "Stripe / Card"),
        ("wechat", "微信支付"),
        ("alipay", "支付宝"),
        ("bank_transfer", "银行转账"),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="orders", verbose_name="关联线索")
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="orders", verbose_name="来源活动")
    intent = models.OneToOneField(IntentEvent, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="order", verbose_name="关联意图")

    funnel_stage = models.CharField("漏斗层级", max_length=2, default="L5", editable=False)

    order_number = models.CharField("订单号", max_length=64, unique=True, db_index=True)
    product_name = models.CharField("产品名称", max_length=200)
    amount = models.DecimalField("支付金额", max_digits=8, decimal_places=2)
    currency = models.CharField("币种", max_length=3, default="USD")
    payment_method = models.CharField("支付方式", max_length=20, choices=PAYMENT_METHOD)

    # 外部交易信息
    transaction_id = models.CharField("交易 ID", max_length=128, blank=True,
        help_text="PayPal / Stripe 返回的 Transaction ID")

    country = CountryField("购买国家", blank=True)
    is_recurring = models.BooleanField("是否为订阅", default=False)

    paid_at = models.DateTimeField("支付时间", default=tz.now)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "L5 付费订单"
        verbose_name_plural = "L5 付费订单"
        ordering = ["-paid_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["paid_at"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return f"[L5] #{self.order_number} - {self.product_name} - ${self.amount} ({self.get_payment_method_display()})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            from uuid import uuid4
            self.order_number = f"YW-{tz.now().strftime('%Y%m%d')}-{uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


# ============================================================
# 邮件 Drip Campaign 配置
# ============================================================

class EmailDrip(models.Model):
    """邮件 Drip Campaign 序列配置"""
    TRIGGER_CHOICES = [
        ("visitor_welcome", "L1 首次访问欢迎"),
        ("engagement_followup", "L2 内容互动跟进"),
        ("lead_welcome", "L3 新线索欢迎"),
        ("report_download", "L3 下载行业报告"),
        ("abandoned_cart", "L4 弃单挽回"),
        ("post_purchase", "L5 购买感谢"),
        ("reengagement", "30天未活跃复购激活"),
    ]

    name = models.CharField("序列名称", max_length=200)
    trigger = models.CharField("触发条件", max_length=30, choices=TRIGGER_CHOICES, unique=True)
    subject_template = models.CharField("邮件主题模板", max_length=300)
    body_template = models.TextField("邮件正文模板",
        help_text="可使用变量: {name}, {email}, {country}, {product_name}")

    # 时间控制
    delay_hours = models.PositiveIntegerField("延迟小时数", default=0,
        help_text="触发后延迟多久发送 (0 = 立即)")
    is_active = models.BooleanField("启用", default=True)

    # GDPR 合规
    include_unsubscribe = models.BooleanField("包含退订链接", default=True)
    gdpr_compliant = models.BooleanField("GDPR 合规", default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "邮件序列"
        verbose_name_plural = "邮件序列"
        ordering = ["trigger"]

    def __str__(self):
        return f"{self.name} [{self.get_trigger_display()}]"


class EmailLog(models.Model):
    """邮件发送日志"""
    STATUS_CHOICES = [
        ("sent", "已发送"),
        ("delivered", "已送达"),
        ("opened", "已打开"),
        ("clicked", "已点击"),
        ("bounced", "退回"),
        ("unsubscribed", "已退订"),
        ("failed", "发送失败"),
    ]

    drip = models.ForeignKey(EmailDrip, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="logs", verbose_name="关联序列")
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
        related_name="email_logs", verbose_name="收件线索")

    subject = models.CharField("邮件主题", max_length=300)
    status = models.CharField("发送状态", max_length=20, choices=STATUS_CHOICES, default="sent")
    error_message = models.TextField("错误信息", blank=True)

    opened_at = models.DateTimeField("打开时间", null=True, blank=True)
    clicked_at = models.DateTimeField("点击时间", null=True, blank=True)

    created_at = models.DateTimeField("发送时间", auto_now_add=True)

    class Meta:
        verbose_name = "邮件日志"
        verbose_name_plural = "邮件日志"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[Email] {self.lead.email} - {self.subject[:40]} ({self.get_status_display()})"
