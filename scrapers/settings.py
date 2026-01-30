BOT_NAME = "scrapers"

SPIDER_MODULES = ["scrapers.spiders"]
NEWSPIDER_MODULE = "scrapers.spiders"

# 1. Отключаем robots.txt (уже сделано, оставляем)
ROBOTSTXT_OBEY = False

# 2. Имитируем реальный браузер (User-Agent помощнее)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# 3. Включаем куки (важно для обхода проверок)
COOKIES_ENABLED = True

# 4. Ограничиваем параллельность (чтобы не забанили за агрессивность)
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 3.5  # Базовая задержка между запросами 2 секунды
RANDOMIZE_DOWNLOAD_DELAY = True

# 5. Добавляем реалистичные заголовки браузера
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
   "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
   "Referer": "https://www.google.com/",
}

# 6. Настройка сохранения в JSON (ваша настройка, оставляем)

FEEDS = {
    'data/book24_raw.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
        'overwrite': True,
    },
    'data/chitai_gorod_raw.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
        'overwrite': True,
    },
    'FEEDS': {
        'data/moscow_raw.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'indent': 4,
            'overwrite': True,
        }
    }
}

# 7. Включаем AutoThrottle (автоматическое управление скоростью)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0  # Начальная задержка
AUTOTHROTTLE_MAX_DELAY = 15.0  # Максимальная задержка при торможении сервера
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Один запрос в один момент времени
AUTOTHROTTLE_DEBUG = False # Поставьте True, если хотите видеть статистику задержек в консоли

# Стандартная кодировка
FEED_EXPORT_ENCODING = "utf-8"