import re
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst,MapCompose


class ItemDataCleaner:
    def extract_book_code(book_page_url):
        pattern = r"jbook_code=(\w+)"
        return re.search(pattern,book_page_url).group(1)
    
    def clean_author(book_author):
        clean_str = '[by] በ'
        return book_author.replace(clean_str,'')\
                            .replace('  ',' ').strip()
    
    def extract_price(price_value):
        pattern = r'\d+'
        match = re.search(pattern, str(price_value))
        if match:
            return int(match.group())
        else:
            return None

    def img_full_url(img_relative_url):
        base_url = 'https://www.jaferbooks.com/'
        return base_url+img_relative_url

    def clean_language(language_value: str):
        return language_value.replace('Language:','').strip()

    def stoke_status(status_value):
        if 'In' in status_value:
            return '1'
        else:
            return '0'

class BookItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    code_in = MapCompose(ItemDataCleaner.extract_book_code)
    author_in = MapCompose(ItemDataCleaner.clean_author)
    etb_price_in = MapCompose(ItemDataCleaner.extract_price)
    usd_price_in = MapCompose(ItemDataCleaner.extract_price)
    category_in = MapCompose(lambda category_name: category_name.strip())
    img_url_in = MapCompose(ItemDataCleaner.img_full_url)
    language_in = MapCompose(ItemDataCleaner.clean_language)
    status_in = MapCompose(ItemDataCleaner.stoke_status)


