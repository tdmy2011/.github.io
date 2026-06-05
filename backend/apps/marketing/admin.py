# -*- coding: utf-8 -*-
"""
Marketing App -- Django Admin 定制
Geo 全球获客营销后台：仪表盘、线索池、UTM 追踪、自动化规则
"""

from django.contrib import admin
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.utils.html import format_html
from django.urls import path
from django.http import JsonResponse
from datetime import timedelta

from .models import Campaign, VisitorLog, Lead


# ============================================================
# 自定义 Dashboard View
# ============================================================

def marketing_dashboard(request):
    """营销仪表盘 JSON 数据"""
    today = timezone.now().date()
    days_7 = today - timedelta(days=7)

    # 访客趋势 (近7天)
    from django.db.models.functions import TruncDate
    daily_visitors = (
        VisitorLog.objects.filter(first_visited__date__gte=days_7)
        .annotate(day=TruncDate("first_visited"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # 国家分布 Top 10
    country_stats = (
        VisitorLog.objects.values("country")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # 今日概览
    today_visitors = VisitorLog.objects.filter(first_visited__date=today).count()
    total_leads = Lead.objects.count()
    active_campaigns = Campaign.objects.filter(status="active").count()
    today_leads = Lead.objects.filter(created_at__date=today).count()

    return JsonResponse({
        "overview": {
            "today_visitors": today_visitors,
            "total_leads": total_leads,
            "active_campaigns": active_campaigns,
            "today_leads": today_leads,
        },
        "daily_visitors": [
            {"date": str(d["day"]), "count": d["count"]}
            for d in daily_visitors
        ],
        "top_countries": [
            {"country": str(c["country"]), "count": c["count"]}
            for c in country_stats
        ],
    })


# ============================================================
# Campaign Admin
# ============================================================

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        "name", "status_badge", "country_tags", "utm_source",
        "leads_count", "visitors_count", "roi_display", "created_at",
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
    leads_count.short_description = "线索"

    def visitors_count(self, obj):
        return obj.visitors.count()
    visitors_count.short_description = "访客"

    def roi_display(self, obj):
        roi = obj.roi
        color = "#10b981" if roi > 0 else "#ef4444"
        return format_html(f'<span style="color:{color};font-weight:bold;">{roi}%</span>')
    roi_display.short_description = "ROI 估算"


# ============================================================
# VisitorLog Admin
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
    readonly_fields = ["ip_hash", "first_visited", "last_seen"]

    fieldsets = (
        ("地理位置", {
            "fields": ("country", "city", "region", "timezone"),
        }),
        ("隐私与合规", {
            "fields": ("ip_hash", "is_gdpr_region", "ip_address"),
            "classes": ("collapse",),
        }),
        ("设备信息", {
            "fields": ("device_type", "browser", "os"),
        }),
        ("流量来源", {
            "fields": (
                "referrer", "referrer_domain", "landing_page",
                "utm_source", "utm_medium", "utm_campaign",
                "utm_term", "utm_content",
            ),
        }),
        ("关联", {
            "fields": ("campaign", "visit_count"),
        }),
    )

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
        if obj.landing_page:
            return obj.landing_page[:60]
        return "-"
    landing_page_short.short_description = "着陆页"

    def utm_combo(self, obj):
        parts = [p for p in [obj.utm_source, obj.utm_medium, obj.utm_campaign] if p]
        return " / ".join(parts) if parts else "-"
    utm_combo.short_description = "UTM"

    def has_lead(self, obj):
        if hasattr(obj, "lead"):
            return format_html('<span style="color:#10b981;">✅</span>')
        return format_html('<span style="color:#94a3b8;">—</span>')
    has_lead.short_description = "已转化"

    def is_gdpr(self, obj):
        if obj.is_gdpr_region:
            return format_html('<span style="color:#f59e0b;">🔒 GDPR</span>')
        return "—"
    is_gdpr.short_description = "隐私"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard-data/", self.admin_site.admin_view(marketing_dashboard),
                 name="marketing-dashboard-data"),
        ]
        return custom_urls + urls

    change_list_template = "admin/marketing/visitorlog/change_list.html"


# ============================================================
# Lead Admin
# ============================================================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        "email", "name", "company", "country_flag", "stage_badge",
        "source", "campaign_link", "created_at",
    ]
    list_filter = ["stage", "source", "country", "created_at"]
    search_fields = ["email", "name", "company"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("基本信息", {
            "fields": ("email", "name", "company", "job_title", "country", "phone"),
        }),
        ("线索追踪", {
            "fields": ("source", "stage", "interested_product", "campaign", "visitor"),
        }),
        ("时间与备注", {
            "fields": ("notes", "contacted_at", "created_at", "updated_at"),
        }),
    )

    def country_flag(self, obj):
        if obj.country and obj.country.code:
            return f"{obj.country.unicode_flag or ''} {obj.country.name}"
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

    def campaign_link(self, obj):
        if obj.campaign:
            return format_html(
                '<a href="/admin/marketing/campaign/{}/change/">{}</a>',
                obj.campaign.id, obj.campaign.name,
            )
        return "-"
    campaign_link.short_description = "关联活动"
