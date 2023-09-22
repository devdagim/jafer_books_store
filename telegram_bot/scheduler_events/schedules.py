from time import sleep

# schedule
import schedule

# project
from telegram_bot.scraper import book_spider, category_spider
from telegram_bot.helpers.executor import Execute
from telegram_bot.helpers.event_storage import EVENT


# ? event handler
@EVENT.on("new_book_released")
def on_new_book_released():
    # ? post_book_channel
    Execute("controllers.post_controller", "PostController@post").exc()
    # TODO: send notification to user abt the new book


@EVENT.on("book_updated")
def on_book_updated():
    # ? edit book post from the channel
    Execute("controllers.post_controller", "PostController@edit_post").exc()


# emit 'new_book_released'
schedule.every(60).seconds.do(
    Execute("scheduler_events.book_event", "BookEvent@check_new_book_release").exc()
)
logging.info(" check_new_book_release")


# emit 'book_updated'
schedule.every(50).seconds.do(
    Execute("scheduler_events.book_event", "BookEvent@check_book_update").exc()
)


def scraping_job():
    category_spider()
    sleep(30)

    book_spider()


schedule.every(5).minutes.do(scraping_job())


while True:
    schedule.run_pending()
    sleep(5)
