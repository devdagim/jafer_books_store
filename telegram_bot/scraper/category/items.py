from scrapy.item import Item,Field


class CategoryItem(Item):
    category_name = Field()


class SubCategoryItem(Item):
    parent_category_name = Field()
    sub_category_name = Field()