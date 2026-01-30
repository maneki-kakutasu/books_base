import scrapy
from scrapers.items import BookItem
import re
import json

class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/catalog/"]

    custom_settings = {
        'FEEDS': {
            'data/book24_raw.json': {
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
        book_links = response.css('a.product-card__name::attr(href)').getall()
        for link in book_links:
            yield response.follow(link, self.parse_book)

        # Ищем тег <a> с классом pagination__item и _next
        next_page = response.css('a.pagination__item._next::attr(href)').get()

        if next_page:
            self.logger.info(f"--- ПЕРЕХОД НА СЛЕДУЮЩУЮ СТРАНИЦУ: {next_page} ---")
            yield response.follow(next_page, self.parse)
        else:
            self.logger.warning("Кнопка 'Вперед' не найдена!")

    def parse_book(self, response):
        item = BookItem()
        
        # 1. Заголовок
        item['title'] = response.css('h1::text').get('').strip()
        
        # 2. Цена
        price_raw = response.css('.app-price::text').get() or response.css('.product-sidebar-price__main-price::text').get()
        if price_raw:
            item['price'] = float(re.sub(r'\D', '', price_raw))

        # 3. ISBN
        chars = response.css('.product-characteristic__item')
        for char in chars:
            label = char.css('.product-characteristic__label::text').get('').strip()
            value = char.css('.product-characteristic__value ::text').getall() # Берем весь текст внутри значения
            value = "".join(value).strip()

            if 'Автор' in label:
                item['author'] = value
            elif 'ISBN' in label:
                # Оставляем только цифры и X
                item['isbn'] = re.sub(r'[^0-9X]', '', value)
            elif 'Издательство' in label:
                item['publisher'] = value
            elif 'Год издания' in label:
                year_match = re.search(r'\d{4}', value)
                if year_match:
                    item['year'] = int(year_match.group())

        # 4. Ссылка на картинку
        img = response.css('.product-poster__picture img')
        img_url = response.css('img.product-poster__main-image::attr(src)').get() or \
                  response.css('img.product-poster__main-image::attr(data-src)').get() or \
                  response.css('.product-poster__picture img::attr(src)').get()
        
        if img_url and img_url.startswith('//'):
            item['image_url'] = 'https:' + img_url
        else:
            item['image_url'] = img_url

        item['url'] = response.url
        item['website_name'] = 'book24.ru'
        item['description'] = " ".join(response.css('.product-about__text p::text').getall()).strip()

        # Валидация: не отдаем айтем, если нет ISBN
        if item.get('isbn') and item.get('title'):
            yield item
        else:
            self.logger.warning(f"Пропущено (нет ISBN): {response.url}")