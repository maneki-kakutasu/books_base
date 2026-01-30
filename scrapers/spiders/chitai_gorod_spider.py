import scrapy
from scrapers.items import BookItem
import re
import json

class ChitaiGorodSpider(scrapy.Spider):
    name = "chitai_gorod"
    allowed_domains = ["chitai-gorod.ru"]
    # Начинаем с раздела новинок или любого крупного раздела
    start_urls = ["https://www.chitai-gorod.ru/catalog/books/"]

    custom_settings = {
        'FEEDS': {
            'data/chitai_gorod_raw.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        # Собираем ссылки на книги
        # Класс карточки обычно содержит 'product-card'
        book_links = response.css('a.product-card__title::attr(href)').getall()
        for link in book_links:
            yield response.follow(link, self.parse_book)

        # ПАГИНАЦИЯ (строго по вашему скриншоту)
        next_page = response.css('a.chg-app-pagination__button-next::attr(href)').get()

        if next_page:
            self.logger.info(f"--- ЧИТАЙ-ГОРОД: ПЕРЕХОД НА СТР: {next_page} ---")
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        item = BookItem()
        item['website_name'] = 'chitai-gorod.ru'
        item['url'] = response.url
        
        # 1. ЗАГОЛОВОК (берем из мета-тегов, они есть всегда для SEO)
        title = response.xpath("//meta[@property='og:title']/@content").get()
        if title:
            # Чистим от SEO-мусора
            item['title'] = title.split('📖')[0].split('купить книгу')[0].strip()
        else:
            item['title'] = response.css('h1::text').get('').strip()

        # 2. АВТОР (пробуем найти в мета-тегах или через регулярку в коде)
        author = response.xpath("//meta[@name='author']/@content").get()
        if not author:
            # Ищем паттерн "author":{"name":"Имя"} или "authorName":"Имя"
            author_match = re.search(r'\"authors?\"\:\[?\{\"name\"\:\"(.*?)\"', response.text)
            if author_match:
                author = author_match.group(1).encode().decode('unicode-escape') # декодируем юникод
        item['author'] = author

        # 3. ЦЕНА (из мета-тегов)
        price = response.xpath("//meta[@property='product:price:amount']/@content").get()
        if price:
            item['price'] = float(price)

        # 4. ISBN (Брутфорс поиск по всему тексту страницы)
        # Ищем паттерн: "ISBN", потом любые символы, потом 13 цифр
        # Или просто ищем 13 цифр, начинающихся на 978 или 979
        isbn_match = re.search(r'97[89][0-9-]{10,15}', response.text)
        if isbn_match:
            # Очищаем найденное от дефисов
            item['isbn'] = re.sub(r'\D', '', isbn_match.group())
        
        # 5. ОПИСАНИЕ (из мета-тегов)
        item['description'] = response.xpath("//meta[@property='og:description']/@content").get()

        # 6. КАРТИНКА
        item['image_url'] = response.xpath("//meta[@property='og:image']/@content").get()

        # 7. ИЗДАТЕЛЬСТВО
        publisher = response.xpath("//span[contains(text(), 'Издательство')]/following-sibling::span/text()").get()
        if not publisher:
            pub_match = re.search(r'\"publisher\"\:\{\"name\"\:\"(.*?)\"', response.text)
            if pub_match:
                publisher = pub_match.group(1).encode().decode('unicode-escape')
        item['publisher'] = publisher

        # ВАЛИДАЦИЯ
        if item.get('isbn') and len(item['isbn']) >= 10:
            self.logger.info(f"+++ УСПЕХ: {item['title']} (ISBN: {item['isbn']})")
            yield item
        else:
            self.logger.warning(f"--- ПРОПУСК: ISBN не найден в коде страницы {response.url}")