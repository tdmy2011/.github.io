# -*- coding: utf-8 -*-
"""
Geo Visitor Middleware
自动记录每位访客的 IP、国家、设备、来源信息
通过 Celery 异步入库，不阻塞 HTTP 响应
"""

import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# 被忽略的路径（静态文件、管理后台等）
IGNORE_PATHS = (
    "/static/", "/media/", "/admin/",
    "/api/", "/favicon.ico", "/robots.txt",
)


def parse_utm(request):
    """从 request.GET 中提取 UTM 参数"""
    return {
        "utm_source": request.GET.get("utm_source", ""),
        "utm_medium": request.GET.get("utm_medium", ""),
        "utm_campaign": request.GET.get("utm_campaign", ""),
        "utm_term": request.GET.get("utm_term", ""),
        "utm_content": request.GET.get("utm_content", ""),
    }


def get_device_type(user_agent_str):
    """简单的 UA 设备类型检测"""
    ua = user_agent_str.lower() if user_agent_str else ""
    if any(k in ua for k in ("mobile", "android", "iphone", "ipod")):
        return "mobile"
    if "ipad" in ua or ("tablet" in ua):
        return "tablet"
    return "desktop"


class GeoVisitorMiddleware(MiddlewareMixin):
    """
    中间件：对每次页面访问异步记录访客信息
    仅在非 API / 非静态资源路径时工作
    """

    def process_response(self, request, response):
        # 跳过非页面请求
        path = request.path_info
        if any(path.startswith(p) for p in IGNORE_PATHS):
            return response

        # 跳过 bot / crawler
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if any(b in user_agent.lower() for b in ("bot", "crawler", "spider", "scraper")):
            return response

        try:
            self._log_visitor(request, user_agent)
        except Exception:
            logger.exception("GeoVisitorMiddleware failed silently")

        return response

    def _log_visitor(self, request, user_agent):
        import hashlib

        from .tasks import process_visitor

        # 客户端 IP
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded.split(",")[0].strip() if x_forwarded else request.META.get("REMOTE_ADDR")

        # GeoIP 解析 (如果有数据库)
        country_code = ""
        city = ""
        try:
            from django.contrib.gis.geoip2 import GeoIP2
            g = GeoIP2()
            geo_data = g.city(ip)
            if geo_data:
                country_code = geo_data.get("country_code", "")
                city = geo_data.get("city", "")
        except Exception:
            # GeoIP 数据库未安装，走异步 GeoIP2 解析
            pass

        # 设备检测
        device_type = get_device_type(user_agent)

        # Referrer
        referrer = request.META.get("HTTP_REFERER", "")

        # UTM 参数
        utm = parse_utm(request)

        # 异步入库
        process_visitor.delay(
            ip_address=ip or "0.0.0.0",
            country_code=country_code,
            city=city,
            device_type=device_type,
            referrer=referrer,
            landing_page=request.path_info,
            utm_params=utm,
            user_agent=user_agent,
        )
