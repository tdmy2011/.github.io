"""
YigeWorks SaaS Platform -- URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET


# ── GDPR / CAN-SPAM 退订 View ──────────────────────────
@require_GET
def unsubscribe_view(request):
    """
    退订处理 (CAN-SPAM / GDPR 要求)
    访问 /unsubscribe/?email=xxx&token=xxx 即可退订
    """
    from apps.marketing.models import Lead
    email = request.GET.get("email", "").strip().lower()
    if not email:
        return HttpResponse("Missing email parameter", status=400)

    updated = Lead.objects.filter(email=email).update(
        unsubscribed=True
    )
    # 同时记录退订时间
    from django.utils import timezone
    Lead.objects.filter(email=email).update(unsubscribed_at=timezone.now())

    if updated:
        return HttpResponse(
            f"<h2 style='font-family:sans-serif;text-align:center;margin-top:80px;'>"
            f"✅ You have been unsubscribed.<br>"
            f"<small style='color:#666;'>Email: {email}</small></h2>",
            content_type="text/html",
        )
    return HttpResponse(
        "<h2 style='font-family:sans-serif;text-align:center;margin-top:80px;'>"
        "Email not found in our system.</h2>",
        content_type="text/html",
        status=404,
    )


# 自定义 Admin 路径（安全加固，非默认 /admin/）
admin_path = getattr(settings, "ADMIN_PATH", "admin/")

urlpatterns = [
    path(admin_path, admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # GDPR / CAN-SPAM 退订
    path("unsubscribe/", unsubscribe_view, name="unsubscribe"),
]

# Debug 模式：静态文件和 Debug Toolbar
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass
