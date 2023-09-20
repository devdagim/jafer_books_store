from itemadapter import ItemAdapter
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.models.book_model import BookModel
import logging


class BookPipeline:
    category_model = CategoryModel()  # for category_table
    book_model = BookModel()  # for book_table

    def process_item(self, item, spider):
        if item["category"]:
            # splitting category from sub_category
            item["category"] = self.split_category(item["category"])

            # set empty list to store book attr data
            book = list()
            for filed in item:
                book.append(item[filed])

            # save book attr into the db
            self.book_model.save_book(book)

        # must return item for obeying scrapy rule
        return item

    # splitting the category('category_name, sub_category_name')
    # and change the text into category id
    def split_category(self, category_name):
        # splitting the category
        category_parts = category_name.split(",")
        # main category
        main_category = str(category_parts[0]).strip()
        category_id = self.category_model.get_category_id(main_category)

        category_item = self.category_model.get_category_id("Uncategorized")

        if category_id:
            category_item = category_id

        # if it has a sub category
        if len(category_parts) > 1:
            sub_category = category_parts[1].strip()

            sub_category_id = self.category_model.get_category_id(sub_category)

            if sub_category_id:
                category_item = sub_category_id

        return category_item
