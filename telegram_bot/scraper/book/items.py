from scrapy.item import Item,Field

class BookItem(Item):
    code = Field()
    name = Field()
    author = Field()
    etb_price = Field()
    usd_price = Field()
    img_url = Field()
    category = Field()
    language = Field()
    status = Field()