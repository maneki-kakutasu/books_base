import scrapy
from ..items import BookItem
import re

class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    # Начинаем с раздела новинок или бестселлеров, чтобы собрать много данных
    start_urls = ["https://www.labirint.ru/genres/2308/"]

    def parse(self, response):
        # Собираем ссылки на книги
        book_links = response.css('a.product-title-link::attr(href)').getall()
        for link in book_links:
            # response.follow автоматически подставит правильный Referer
            yield response.follow(link, self.parse_book)

        # Пагинация (только если на первой странице всё прошло успешно)
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        title = response.css('h1::text').get()
        if not title:
            return # Пропускаем, если это не страница книги

        item = BookItem()
        item['title'] = title.strip()
        item['author'] = response.css('div.authors a::text').get()
        item['url'] = response.url
        item['website_name'] = 'labirint.ru'
        
        # Цена
        price_raw = response.css('span.buying-priceval-number::text').get()
        if price_raw:
            item['price'] = float(price_raw.replace(' ', ''))
            
        # ISBN - Лабиринт часто прячет его в спец. поле
        # Попробуем найти через текст "ISBN:"
        isbn_text = response.xpath("//div[contains(text(), 'ISBN')]/text()").get()
        if isbn_text:
            item['isbn'] = re.sub(r'\D', '', isbn_text)
        else:
            # Запасной вариант для ISBN
            item['isbn'] = response.css('div.isbn::text').re_first(r'[\d-]+')

        item['description'] = " ".join(response.css('div#product-about p::text').getall()).strip()
        item['image_url'] = response.css('div#product-image img::attr(src)').get()
        
        # Дополнительно: издательство
        item['publisher'] = response.css('div.publisher a::text').get()
        
        yield item