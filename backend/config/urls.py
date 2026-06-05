"""
YigeWorks SaaS Platform -- URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 自定义 Admin 路径（安全加固，非默认 /admin/）
admin_path = getattr(settings, "ADMIN_PATH", "admin/")

urlpatterns = [
    path(admin_path, admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
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
