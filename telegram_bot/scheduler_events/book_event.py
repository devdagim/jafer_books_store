import logging

# project
from telegram_bot.helpers.event_storage import EVENT
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.post_model import PostModel


class BookEvent:
    def check_new_book_release(self):
        post_model = PostModel()
        is_their_new = post_model.check_un_posted_books()
        print("is_their_new",is_their_new)
        logging.info("checking new book release")

        if is_their_new:
            EVENT.emit("new_book_released")
            logging.info("emitting event: new_book_released")

    def check_book_update(self):
        book_model = BookModel()
        is_their_update = book_model.check_updated_books()
        print("is_their_new",is_their_update)
        logging.info("checking book update")

        if is_their_update:
            EVENT.emit("book_updated")
            logging.info("emitting event: book_updated")
