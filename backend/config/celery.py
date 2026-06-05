"""
YigeWorks -- Celery Configuration
文档: https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("yigeworks")

# 从 Django settings 中读取 Celery 配置 (前缀: CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现所有已注册 Django app 中的 tasks.py
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Celery Debug Task: {self.request!r}")
