#!/usr/bin/env bash
set -euo pipefail

# Переходим в директорию проекта (если нужно)
# cd "$(dirname "$0")"

echo "🔍 Проверка кода Ruff..."
ruff check . --fix

echo "✨ Форматирование кода Ruff..."
ruff format .

echo "🗑️ Очистка кэша..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "✅ Готово!"
