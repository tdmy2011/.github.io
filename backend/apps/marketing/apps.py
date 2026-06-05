from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.marketing"
    verbose_name = "🚀 Geo 全球获客营销"

    def ready(self):
        # 注册 Signals
        import apps.marketing.signals  # noqa: F401
