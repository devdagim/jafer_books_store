from math import ceil
import scrapy
from .items import BookItem
from .items_loader import BookItemLoader


class BookSpider(scrapy.Spider):
    name = 'bookSpider'
    base_url = 'https://www.jaferbooks.com/'
    start_urls = ['https://www.jaferbooks.com/shop-grid.php?pn=1']
    shop_url = 'https://www.jaferbooks.com/shop-grid.php?pn='

    def parse(self, response):
        book_page_urls = response.css('.product__content a::attr(href)')

        total_books = response.css('.shop__list__wrapper p b::text')\
                        .get().replace(" Books","")
        shop_end_page = ceil(int(total_books)/16)

        for book_page_url in book_page_urls:
            yield scrapy.Request(url=self.base_url+book_page_url.get(), 
                                callback=self.parse_book)

        for pn in range(1,shop_end_page+1):
            yield response.follow(url=self.shop_url+str(pn), callback=self.parse)

    def parse_book(self, response):
        loader = BookItemLoader(item=BookItem(),selector=response)

        loader.add_value('code', response.url)
        loader.add_css('name','.product__info__main h1::text')
        loader.add_css('author' ,'.product__info__main span > h6::text')
        loader.add_css('etb_price','.price-box h5::text')
        loader.add_css('usd_price','.product__info__main div b::text')
        loader.add_css('img_url','.modal-body img::attr(src)')
        loader.add_css('category','.product_meta a::text')
        loader.add_xpath('language',"//span[contains(text(),'Language:')]/text()")
        loader.add_css('status','.product__info__main div > span b::text')

        items = loader.load_item()
        yield items


