from time import sleep
import logging

# schedule
import schedule

# project
from telegram_bot.scraper import book_spider, category_spider
from telegram_bot.helpers.executor import Execute
from telegram_bot.helpers.event_storage import EVENT

logging.basicConfig(level=logging.INFO)


# ? event handler
@EVENT.on("new_book_released")
def on_new_book_released():
    # ? post_book_channel
    Execute("controllers.post_controller", "PostController@post").exc()


@EVENT.on("book_updated")
def on_book_updated():
    # ? edit book post from the channel
    Execute("controllers.post_controller", "PostController@edit_post").exc()
    print("hello")


# emit 'new_book_released' on success
def check_new_book_release_job():
    Execute("scheduler_events.book_event", "BookEvent@check_new_book_release").exc()


# emit 'book_updated' on success
def check_book_update_job():
    Execute("scheduler_events.book_event", "BookEvent@check_book_update").exc()



# schedule.every().minute.at(":10").do(check_new_book_release_job)
# schedule.every().minute.at(":10").do(check_book_update_job)
schedule.every(1).seconds.do(category_spider)
schedule.every(5).seconds.do(book_spider)


while True:
    schedule.run_pending()
    sleep(1)
