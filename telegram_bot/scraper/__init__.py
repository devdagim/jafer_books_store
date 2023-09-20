from scrapy.crawler import CrawlerProcess
# book_spider
from telegram_bot.scraper.book.book_spider import BookSpider
import telegram_bot.scraper.book.settings as book_setting
# category_spider
from telegram_bot.scraper.category.category_spider import CategorySpider
import telegram_bot.scraper.category.settings as category_setting


def book_spider():
    process = CrawlerProcess(settings=book_setting.SETTINGS)
    process.crawl(BookSpider)
    process.start()


def category_spider():
    process = CrawlerProcess(settings=category_setting.SETTINGS)
    process.crawl(CategorySpider)
    process.start()