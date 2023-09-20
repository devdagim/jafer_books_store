from itemadapter import ItemAdapter
from telegram_bot.models.category_model import CategoryModel


# ? used to save category attr into category table using CategoryModel


class CategoryPipeline:
    model = CategoryModel()

    # scrapy bulletin method
    # called when item are processed and we save data to the db
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # if it have attr category_name it mean it's category data
        if adapter.get("category_name"):
            self.add_category(item)

        elif adapter.get("sub_category_name"):
            self.add_sub_category(item)

        return item

    def add_category(self, item):
        sub_category_parent_id = 0  # for main category
        category_name = item["category_name"]

        self.model.save_category(sub_category_parent_id, category_name)

    def add_sub_category(self, item):
        parent_category_name = item["parent_category_name"]

        sub_category_parent_id = self.model.get_category_id(
            parent_category_name
        )
        sub_category_name = item["sub_category_name"]

        self.model.save_category(sub_category_parent_id, sub_category_name)
