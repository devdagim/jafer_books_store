from scrapy.crawler import CrawlerProcess
from twisted.internet.epollreactor import EPollReactor

# book_spider
from telegram_bot.scraper.book.book_spider import BookSpider
import telegram_bot.scraper.book.settings as book_setting

# category_spider
from telegram_bot.scraper.category.category_spider import CategorySpider
import telegram_bot.scraper.category.settings as category_setting


def category_spider():
    reactor = EPollReactor()
    runner = CrawlerProcess(settings=category_setting.SETTINGS)
    running_spider = runner.crawl(CategorySpider)
    runner.start()

    running_spider.addBoth(lambda _: reactor.stop())
    reactor.run()


def book_spider():
    reactor = EPollReactor()
    runner = CrawlerProcess(settings=book_setting.SETTINGS)
    running_spider = runner.crawl(BookSpider)
    runner.start()

    running_spider.addBoth(lambda _: reactor.stop())
    reactor.run()
