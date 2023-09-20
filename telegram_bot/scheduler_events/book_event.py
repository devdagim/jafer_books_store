from telegram_bot.helpers.event_storage import EVENT
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.post_model import PostModel


class BookEvent:
    def check_new_book_release(self):
        post_model = PostModel()
        is_their_new = post_model.check_unposted_books()

        if is_their_new:
            EVENT.emit('new_book_released')

    def check_book_update(self):
        book_model = BookModel()
        is_their_update = book_model.check_updated_books()

        if is_their_update:
            EVENT.emit('book_updated')