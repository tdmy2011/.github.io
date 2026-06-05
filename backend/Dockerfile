# ============================================================
# YigeWorks SaaS Platform -- Dockerfile
# ============================================================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 系统依赖 (psycopg2 + GeoIP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libgeoip-dev \
    geoip-database \
    && rm -rf /var/lib/apt/lists/*

# Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 应用代码
COPY . .

# 静态文件收集
RUN mkdir -p /app/staticfiles /app/media /app/logs

EXPOSE 8000

# Gunicorn 生产级启动
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gthread", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
