# ===== 1. Образ =====
FROM python:3.13-slim

# ===== 2. Настройка окружения =====
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ===== 3. Установка зависимостей =====
# Сначала копируем requirements.txt, чтобы использовать кеш при сборке
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ===== 4. Копируем исходники =====
COPY src/ .

# ===== 5. Команда запуска =====
CMD ["python", "-m", "src.main"]