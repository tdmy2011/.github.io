# -*- coding: utf-8 -*-
"""
Marketing App -- Django Admin 定制
Geo 全球获客营销后台 · 5 层漏斗可视化仪表盘

功能:
  - 全球访客热力图 (Chart.js)
  - 各国转化率柱状图
  - UTM 渠道 ROI 排行
  - 漏斗健康度面板
  - 5 层漏斗数据 Admin 面板
  - 邮件 Drip 序列管理
"""

from django.contrib import admin
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from django.utils.html import format_html
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from datetime import timedelta

from .models import (
    Campaign, VisitorLog, Lead, ContentEngagement,
    IntentEvent, Order, EmailDrip, EmailLog,
)


# ============================================================
# Admin Dashboard 数据 API
# ============================================================

def marketing_dashboard_data(request):
    """实时营销仪表盘 JSON 数据 API"""
    from django.db.models.functions import TruncDate

    days = int(request.GET.get("days", 30))
    today = timezone.now().date()
    start_date = today - timedelta(days=days)

    # ── 漏斗各层数量 ──────────────────────────────
    l1 = VisitorLog.objects.filter(first_visited__date__gte=start_date).count()
    l2 = ContentEngagement.objects.filter(
        created_at__date__gte=start_date, is_qualified=True).count()
    l3 = Lead.objects.filter(created_at__date__gte=start_date).count()
    l4 = IntentEvent.objects.filter(created_at__date__gte=start_date).count()
    l5 = Order.objects.filter(paid_at__date__gte=start_date).count()
    revenue = Order.objects.filter(paid_at__date__gte=start_date).aggregate(
        total=Sum("amount"))["total"] or 0

    # ── 日访客趋势 ────────────────────────────────
    daily_visitors = (
        VisitorLog.objects.filter(first_visited__date__gte=start_date)
        .annotate(day=TruncDate("first_visited"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # ── 国家 Top 10 访客数 ────────────────────────
    country_visitors = (
        VisitorLog.objects.filter(first_visited__date__gte=start_date)
        .values("country")
        .annotate(visitors=Count("id"))
        .order_by("-visitors")[:10]
    )

    # ── 各国转化率 (L5 / L1) ──────────────────────
    country_orders = (
        Order.objects.filter(paid_at__date__gte=start_date)
        .values("country")
        .annotate(orders=Count("id"))
        .order_by("-orders")[:10]
    )
    order_map = {o["country"]: o["orders"] for o in country_orders}

    country_conversion = []
    for c in country_visitors:
        code = str(c["country"])
        orders = order_map.get(code, 0)
        conversion = round(orders / c["visitors"] * 100, 2) if c["visitors"] else 0
        country_conversion.append({
            "country": code,
            "visitors": c["visitors"],
            "orders": orders,
            "conversion_rate": conversion,
        })

    # ── UTM 渠道 ROI ──────────────────────────────
    utm_stats = (
        Lead.objects.filter(created_at__date__gte=start_date)
        .exclude(visitor__utm_source="")
        .values("visitor__utm_source", "visitor__utm_medium")
        .annotate(leads=Count("id"))
        .order_by("-leads")[:10]
    )

    # ── 邮件发送统计 ──────────────────────────────
    email_total = EmailLog.objects.filter(created_at__date__gte=start_date).count()
    email_opened = EmailLog.objects.filter(
        created_at__date__gte=start_date, opened_at__isnull=False).count()
    email_open_rate = round(email_opened / email_total * 100, 1) if email_total else 0

    # ── 今日概览 ──────────────────────────────────
    today_visitors = VisitorLog.objects.filter(first_visited__date=today).count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    today_orders = Order.objects.filter(paid_at__date=today).count()
    today_revenue = Order.objects.filter(paid_at__date=today).aggregate(
        total=Sum("amount"))["total"] or 0

    return JsonResponse({
        "period_days": days,
        "overview": {
            "today_visitors": today_visitors,
            "today_leads": today_leads,
            "today_orders": today_orders,
            "today_revenue": float(today_revenue),
        },
        "funnel": {
            "L1": l1, "L2": l2, "L3": l3, "L4": l4, "L5": l5,
            "L1_to_L3_rate": f"{round(l3/l1*100,2)}%" if l1 else "0%",
            "L1_to_L5_rate": f"{round(l5/l1*100,2)}%" if l1 else "0%",
        },
        "revenue_usd": float(revenue),
        "daily_visitors": [
            {"date": str(d["day"]), "count": d["count"]} for d in daily_visitors
        ],
        "country_conversion": country_conversion,
        "utm_stats": [
            {"source": u["visitor__utm_source"],
             "medium": u["visitor__utm_medium"],
             "leads": u["leads"]} for u in utm_stats
        ],
        "email": {
            "total_sent": email_total,
            "open_rate": email_open_rate,
        },
    })


# ============================================================
# Custom Admin Site Dashboard
# ============================================================

class MarketingAdminSite(admin.AdminSite):
    """营销专属 Admin 站点 (可选, 与主站并存)"""
    site_header = "🌍 YigeWorks 全球营销中台"
    site_title = "YigeWorks Marketing"
    index_title = "Geo 全球获客 · 转化漏斗 · 邮件触达"


# ============================================================
# Campaign Admin
# ============================================================

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        "name", "status_badge", "country_tags", "utm_source",
        "leads_count", "visitors_count", "orders_count",
        "roi_display", "conversion_rate_display", "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "utm_source", "utm_campaign"]
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("基本信息", {
            "fields": ("name", "slug", "status", "description"),
        }),
        ("UTM 追踪", {
            "fields": ("utm_source", "utm_medium", "utm_campaign"),
        }),
        ("自动化营销规则", {
            "fields": (
                "auto_rule_enabled", "target_countries",
                "target_page_pattern", "delay_minutes",
                "welcome_email_template",
            ),
        }),
        ("预算", {
            "fields": ("budget", "spent"),
        }),
    )

    def status_badge(self, obj):
        colors = {"active": "#10b981", "paused": "#f59e0b", "draft": "#94a3b8", "ended": "#64748b"}
        color = colors.get(obj.status, "#94a3b8")
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:12px;'
            'background:{};color:#fff;font-size:12px;">{}</span>',
            color, obj.get_status_display(),
        )
    status_badge.short_description = "状态"

    def country_tags(self, obj):
        if not obj.target_countries:
            return "-"
        return ", ".join(obj.target_countries[:5])
    country_tags.short_description = "目标国家"

    def leads_count(self, obj):
        return obj.leads.count()
    leads_count.short_description = "L3 线索"

    def visitors_count(self, obj):
        return obj.visitors.count()
    visitors_count.short_description = "L1 访客"

    def orders_count(self, obj):
        return obj.orders.count()
    orders_count.short_description = "L5 订单"

    def roi_display(self, obj):
        roi = obj.roi
        color = "#10b981" if roi > 0 else "#ef4444"
        return format_html('<span style="color:{};font-weight:bold;">{:.1f}%</span>', color, roi)
    roi_display.short_description = "ROI"

    def conversion_rate_display(self, obj):
        rate = obj.conversion_rate
        color = "#10b981" if rate > 0 else "#94a3b8"
        return format_html('<span style="color:{};font-weight:bold;">{:.2f}%</span>', color, rate)
    conversion_rate_display.short_description = "L1→L5 转化"


# ============================================================
# VisitorLog Admin (L1) — 含全局仪表盘
# ============================================================

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = [
        "country_flag", "city", "device_icon", "landing_page_short",
        "utm_combo", "has_lead", "is_gdpr", "first_visited",
    ]
    list_filter = ["country", "device_type", "is_gdpr_region", "first_visited"]
    search_fields = ["city", "landing_page", "utm_source", "ip_hash"]
    date_hierarchy = "first_visited"
    readonly_fields = ["ip_hash", "first_visited", "last_seen", "funnel_stage"]

    def country_flag(self, obj):
        if obj.country and obj.country.code:
            return format_html(
                '<span title="{}">{} {}</span>',
                obj.country.name,
                obj.country.unicode_flag or "",
                obj.country.name or obj.country.code,
            )
        return "-"
    country_flag.short_description = "国家"

    def device_icon(self, obj):
        icons = {"mobile": "📱", "tablet": "📋", "desktop": "💻", "other": "❓"}
        return icons.get(obj.device_type, "❓")
    device_icon.short_description = "设备"

    def landing_page_short(self, obj):
        return (obj.landing_page[:60] + "...") if len(obj.landing_page) > 60 else obj.landing_page or "-"
    landing_page_short.short_description = "着陆页"

    def utm_combo(self, obj):
        parts = [p for p in [obj.utm_source, obj.utm_medium, obj.utm_campaign] if p]
        return " / ".join(parts) if parts else "-"
    utm_combo.short_description = "UTM"

    def has_lead(self, obj):
        if hasattr(obj, "lead"):
            return format_html('<span style="color:#10b981;">✅ L3</span>')
        return format_html('<span style="color:#94a3b8;">—</span>')
    has_lead.short_description = "转化"

    def is_gdpr(self, obj):
        if obj.is_gdpr_region:
            return format_html('<span style="color:#f59e0b;">🔒 GDPR</span>')
        return "—"
    is_gdpr.short_description = "隐私"

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("geo-dashboard/",
                 self.admin_site.admin_view(marketing_dashboard_data),
                 name="marketing-dashboard-data"),
        ]
        return extra_urls + urls

    change_list_template = "admin/marketing/visitorlog/change_list.html"


# ============================================================
# ContentEngagement Admin (L2)
# ============================================================

@admin.register(ContentEngagement)
class ContentEngagementAdmin(admin.ModelAdmin):
    list_display = [
        "visitor_country", "engagement_type", "content_title_short",
        "duration_display", "is_qualified", "created_at",
    ]
    list_filter = ["engagement_type", "is_qualified", "country", "created_at"]
    search_fields = ["content_title", "content_url"]
    readonly_fields = ["funnel_stage"]

    def visitor_country(self, obj):
        flag = obj.visitor.country.unicode_flag if obj.visitor.country else ""
        name = obj.visitor.country.name if obj.visitor.country else "Unknown"
        return format_html('<span title="{}">{} {}</span>', name, flag, name)
    visitor_country.short_description = "国家"

    def content_title_short(self, obj):
        return obj.content_title[:50] or obj.content_url[:50] or "-"
    content_title_short.short_description = "内容"

    def duration_display(self, obj):
        if obj.duration_seconds >= 60:
            return format_html(
                '<span style="color:#10b981;font-weight:bold;">{}s ✓</span>',
                obj.duration_seconds)
        return format_html('<span style="color:#94a3b8;">{}s</span>', obj.duration_seconds)
    duration_display.short_description = "停留时长"


# ============================================================
# Lead Admin (L3)
# ============================================================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        "email", "name", "company", "country_flag", "stage_badge",
        "source_badge", "campaign_link", "email_status", "consent_display", "created_at",
    ]
    list_filter = ["stage", "source", "country", "consent_marketing", "unsubscribed", "created_at"]
    search_fields = ["email", "name", "company"]
    readonly_fields = ["created_at", "updated_at", "funnel_stage"]

    fieldsets = (
        ("基本信息", {
            "fields": ("email", "name", "company", "job_title", "country", "phone"),
        }),
        ("线索追踪", {
            "fields": ("source", "source_page", "stage", "interested_product", "campaign", "visitor"),
        }),
        ("邮件触达状态", {
            "fields": (
                "email_sent_welcome", "email_sent_report", "email_sent_discount",
            ),
        }),
        ("GDPR / CAN-SPAM 合规", {
            "fields": (
                "consent_marketing", "consent_timestamp",
                "unsubscribed", "unsubscribed_at",
            ),
            "classes": ("collapse",),
        }),
        ("时间与备注", {
            "fields": ("notes", "contacted_at", "created_at", "updated_at"),
        }),
    )

    actions = ["mark_contacted", "send_welcome_now", "export_to_csv"]

    def country_flag(self, obj):
        if obj.country and obj.country.code:
            return format_html("{} {}", obj.country.unicode_flag or "", obj.country.name)
        return "-"
    country_flag.short_description = "国家"

    def stage_badge(self, obj):
        colors = {
            "new": "#3b82f6", "contacted": "#8b5cf6",
            "qualified": "#f59e0b", "converted": "#10b981", "closed": "#ef4444",
        }
        color = colors.get(obj.stage, "#94a3b8")
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:12px;'
            'background:{};color:#fff;font-size:12px;">{}</span>',
            color, obj.get_stage_display(),
        )
    stage_badge.short_description = "阶段"

    def source_badge(self, obj):
        icons = {
            "website": "🌐", "youtube": "▶️", "linkedin": "💼",
            "facebook": "📘", "referral": "🤝", "event": "🎤",
            "ad": "📢", "organic": "🔍",
        }
        icon = icons.get(obj.source, "")
        return f"{icon} {obj.get_source_display()}"
    source_badge.short_description = "渠道"

    def campaign_link(self, obj):
        if obj.campaign:
            return format_html(
                '<a href="/admin/marketing/campaign/{}/change/">{}</a>',
                obj.campaign.id, obj.campaign.name,
            )
        return "-"
    campaign_link.short_description = "活动"

    def email_status(self, obj):
        parts = []
        if obj.email_sent_welcome:
            parts.append("✉️")
        if obj.email_sent_report:
            parts.append("📄")
        if obj.email_sent_discount:
            parts.append("🎁")
        return " ".join(parts) if parts else "—"
    email_status.short_description = "已发邮件"

    def consent_display(self, obj):
        if obj.unsubscribed:
            return format_html('<span style="color:#ef4444;">退订</span>')
        if obj.consent_marketing:
            return format_html('<span style="color:#10b981;">✅ 已授权</span>')
        return format_html('<span style="color:#94a3b8;">未授权</span>')
    consent_display.short_description = "邮件授权"

    def mark_contacted(self, request, queryset):
        queryset.update(stage="contacted", contacted_at=timezone.now())
    mark_contacted.short_description = "标记为已联系"

    def send_welcome_now(self, request, queryset):
        from .tasks import send_welcome_email
        count = 0
        for lead in queryset:
            send_welcome_email.delay(lead.id)
            count += 1
        self.message_user(request, f"已排队发送 {count} 封欢迎邮件")
    send_welcome_now.short_description = "立即发送欢迎邮件"

    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="leads_export.csv"'
        response.write("\ufeff")  # BOM for Excel
        writer = csv.writer(response)
        writer.writerow(["Email", "Name", "Company", "Country", "Stage", "Source", "Created At"])
        for lead in queryset:
            writer.writerow([
                lead.email, lead.name, lead.company,
                str(lead.country), lead.get_stage_display(),
                lead.get_source_display(), lead.created_at.strftime("%Y-%m-%d %H:%M"),
            ])
        return response
    export_to_csv.short_description = "导出 CSV"


# ============================================================
# IntentEvent Admin (L4)
# ============================================================

@admin.register(IntentEvent)
class IntentEventAdmin(admin.ModelAdmin):
    list_display = [
        "intent_type_badge", "product_name", "product_price",
        "country_flag", "lead_link", "is_completed", "abandoned_badge", "created_at",
    ]
    list_filter = ["intent_type", "is_completed", "country", "created_at"]
    search_fields = ["product_name", "lead__email"]
    readonly_fields = ["funnel_stage"]

    def intent_type_badge(self, obj):
        icons = {
            "pricing_view": "💰", "add_to_cart": "🛒",
            "checkout_start": "💳", "trial_request": "🆓",
            "consultation": "📞", "demo_request": "🎥",
        }
        icon = icons.get(obj.intent_type, "")
        return format_html("{} {}", icon, obj.get_intent_type_display())
    intent_type_badge.short_description = "意图"

    def country_flag(self, obj):
        if obj.country and obj.country.code:
            return format_html("{} {}", obj.country.unicode_flag or "", obj.country.name)
        return "-"
    country_flag.short_description = "国家"

    def lead_link(self, obj):
        if obj.lead:
            return format_html(
                '<a href="/admin/marketing/lead/{}/change/">{}</a>',
                obj.lead.id, obj.lead.email,
            )
        return "-"
    lead_link.short_description = "线索"

    def abandoned_badge(self, obj):
        if obj.is_abandoned:
            return format_html('<span style="color:#ef4444;">⚠️ 弃单</span>')
        return "—"
    abandoned_badge.short_description = "弃单"


# ============================================================
# Order Admin (L5)
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number", "product_name", "amount_display",
        "payment_method_badge", "country_flag", "lead_link",
        "campaign_link", "paid_at",
    ]
    list_filter = ["payment_method", "country", "is_recurring", "paid_at"]
    search_fields = ["order_number", "product_name", "transaction_id", "lead__email"]
    readonly_fields = ["order_number", "funnel_stage", "created_at"]
    date_hierarchy = "paid_at"

    def amount_display(self, obj):
        return format_html(
            '<span style="font-weight:bold;color:#10b981;">{} {}</span>',
            obj.currency, obj.amount,
        )
    amount_display.short_description = "金额"

    def payment_method_badge(self, obj):
        icons = {
            "paypal": "🅿️ PayPal", "stripe": "💳 Stripe",
            "wechat": "🟢 微信", "alipay": "🔵 支付宝",
            "bank_transfer": "🏦 银行",
        }
        return icons.get(obj.payment_method, obj.get_payment_method_display())
    payment_method_badge.short_description = "支付方式"

    def country_flag(self, obj):
        if obj.country and obj.country.code:
            return format_html("{} {}", obj.country.unicode_flag or "", obj.country.name)
        return "-"
    country_flag.short_description = "购买国家"

    def lead_link(self, obj):
        if obj.lead:
            return format_html(
                '<a href="/admin/marketing/lead/{}/change/">{}</a>',
                obj.lead.id, obj.lead.email,
            )
        return "-"
    lead_link.short_description = "客户"

    def campaign_link(self, obj):
        if obj.campaign:
            return format_html(
                '<a href="/admin/marketing/campaign/{}/change/">{}</a>',
                obj.campaign.id, obj.campaign.name,
            )
        return "-"
    campaign_link.short_description = "来源活动"


# ============================================================
# EmailDrip Admin
# ============================================================

@admin.register(EmailDrip)
class EmailDripAdmin(admin.ModelAdmin):
    list_display = [
        "name", "trigger_badge", "is_active", "delay_hours",
        "gdpr_badge", "sent_count", "open_rate",
    ]
    list_filter = ["is_active", "trigger", "gdpr_compliant"]
    search_fields = ["name", "subject_template"]

    def trigger_badge(self, obj):
        return obj.get_trigger_display()
    trigger_badge.short_description = "触发条件"

    def gdpr_badge(self, obj):
        if obj.gdpr_compliant:
            return format_html('<span style="color:#10b981;">🔒 GDPR</span>')
        return format_html('<span style="color:#ef4444;">⚠️ 待合规</span>')
    gdpr_badge.short_description = "合规"

    def sent_count(self, obj):
        return obj.logs.count()
    sent_count.short_description = "已发"

    def open_rate(self, obj):
        total = obj.logs.count()
        if not total:
            return "-"
        opened = obj.logs.filter(opened_at__isnull=False).count()
        return f"{round(opened/total*100, 1)}%"
    open_rate.short_description = "打开率"


# ============================================================
# EmailLog Admin
# ============================================================

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = [
        "lead_email", "subject_short", "status_badge",
        "drip_name", "opened_at", "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["lead__email", "subject"]
    readonly_fields = ["created_at", "opened_at", "clicked_at"]

    def lead_email(self, obj):
        return format_html(
            '<a href="/admin/marketing/lead/{}/change/">{}</a>',
            obj.lead.id, obj.lead.email,
        )
    lead_email.short_description = "收件人"

    def subject_short(self, obj):
        return obj.subject[:50]
    subject_short.short_description = "主题"

    def status_badge(self, obj):
        colors = {
            "sent": "#3b82f6", "delivered": "#06b6d4", "opened": "#10b981",
            "clicked": "#8b5cf6", "bounced": "#f59e0b",
            "unsubscribed": "#94a3b8", "failed": "#ef4444",
        }
        color = colors.get(obj.status, "#94a3b8")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:8px;'
            'background:{};color:#fff;font-size:11px;">{}</span>',
            color, obj.get_status_display(),
        )
    status_badge.short_description = "状态"

    def drip_name(self, obj):
        return obj.drip.name if obj.drip else "-"
    drip_name.short_description = "序列"
