# -*- coding: utf-8 -*-
"""
YigeWorks SaaS Platform -- Marketing App Models
Geo 全球获客营销：VisitorLog、Campaign、Lead
依赖：django-countries，GeoIP2
"""

from django.db import models
from django.utils import timezone as tz
from django_countries.fields import CountryField


class Campaign(models.Model):
    """推广活动"""
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

    # UTM 自动化
    utm_source = models.CharField("UTM Source", max_length=120, blank=True)
    utm_medium = models.CharField("UTM Medium", max_length=120, blank=True)
    utm_campaign = models.CharField("UTM Campaign", max_length=120, blank=True)

    # 自动化规则
    auto_rule_enabled = models.BooleanField("启用自动规则", default=False)
    target_countries = models.JSONField("目标国家", default=list, blank=True,
        help_text="例如: ['US', 'GB', 'VN', 'TH']")
    target_page_pattern = models.CharField("目标页面匹配", max_length=200, blank=True,
        help_text="例如: /pricing/ 匹配所有定价页访问")
    delay_minutes = models.PositiveIntegerField("延迟分钟数", default=10)
    welcome_email_template = models.TextField("欢迎邮件模板", blank=True)

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
        """简单 ROI 计算"""
        if self.spent == 0:
            return 0
        leads = self.leads.count()
        return round((leads * 50 - float(self.spent)) / float(self.spent) * 100, 1)


class VisitorLog(models.Model):
    """全球访客日志"""
    DEVICE_CHOICES = [
        ("mobile", "手机"),
        ("tablet", "平板"),
        ("desktop", "桌面"),
        ("other", "其他"),
    ]

    ip_address = models.GenericIPAddressField("IP 地址", null=True, blank=True)
    ip_hash = models.CharField("IP 哈希 (GDPR)", max_length=64, blank=True, db_index=True,
        help_text="SHA-256 哈希后的 IP，满足 GDPR 要求")
    country = CountryField("国家/地区", blank=True, blank_label="(未知)")
    city = models.CharField("城市", max_length=100, blank=True)
    region = models.CharField("省/州", max_length=100, blank=True)
    timezone = models.CharField("时区", max_length=50, blank=True)

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

    is_gdpr_region = models.BooleanField("GDPR 地区", default=False,
        help_text="是否来自 EU/EEA 或英国")

    first_visited = models.DateTimeField("首次访问", default=tz.now)
    last_seen = models.DateTimeField("最近活跃", auto_now=True)
    visit_count = models.PositiveIntegerField("访问次数", default=1)

    class Meta:
        verbose_name = "访客日志"
        verbose_name_plural = "访客日志"
        ordering = ["-first_visited"]
        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["ip_hash"]),
            models.Index(fields=["first_visited"]),
        ]

    def __str__(self):
        return f"{self.country.name or 'Unknown'} - {self.ip_hash[:8] if self.ip_hash else 'NoIP'} - {self.first_visited.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        import hashlib
        if self.ip_address and not self.ip_hash:
            self.ip_hash = hashlib.sha256(self.ip_address.encode()).hexdigest()
        # GDPR 地区检测
        gdpr_countries = {"AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR",
                          "HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK",
                          "SI","ES","SE","GB","IS","LI","NO","CH"}
        if self.country and self.country.code in gdpr_countries:
            self.is_gdpr_region = True
        super().save(*args, **kwargs)


class Lead(models.Model):
    """营销线索"""
    STAGE_CHOICES = [
        ("new", "新线索"),
        ("contacted", "已联系"),
        ("qualified", "已确认"),  # 有购买意向
        ("converted", "已转化"),
        ("closed", "已关闭"),
    ]

    email = models.EmailField("邮箱", unique=True)
    name = models.CharField("姓名", max_length=200, blank=True)
    company = models.CharField("公司", max_length=200, blank=True)
    job_title = models.CharField("职位", max_length=200, blank=True)

    country = CountryField("国家/地区", blank=True)
    phone = models.CharField("电话", max_length=30, blank=True)

    source = models.CharField("来源", max_length=100, blank=True,
        help_text="website / youtube / linkedin / referral / event")
    stage = models.CharField("阶段", max_length=20, choices=STAGE_CHOICES, default="new")

    # 关联
    visitor = models.OneToOneField(VisitorLog, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="lead", verbose_name="关联访客")
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leads", verbose_name="来源活动")

    interested_product = models.CharField("感兴趣产品", max_length=200, blank=True)
    notes = models.TextField("备注", blank=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    contacted_at = models.DateTimeField("联系时间", null=True, blank=True)

    class Meta:
        verbose_name = "营销线索"
        verbose_name_plural = "营销线索"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} - {self.get_stage_display()}"
