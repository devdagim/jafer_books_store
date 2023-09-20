import scrapy
from .items import CategoryItem, SubCategoryItem
from .items_loader import CategoryItemLoader, SubCategoryItemLoader


class CategorySpider(scrapy.Spider):
    name = "categorySpider"
    base_url = "https://www.jaferbooks.com/"
    start_urls = ["https://www.jaferbooks.com/shop-grid.php"]

    def parse(self, response):
        categories = response.css("aside.poroduct--cat a")
        for category in categories:
            loader = CategoryItemLoader(item=CategoryItem(), selector=category)
            loader.add_css("category_name", "::text")

            category_items = loader.load_item()
            yield category_items

            sub_category_page_link = category.css("::attr(href)").get()
            category_name = category.css("::text").get()

            yield scrapy.Request(
                url=self.base_url + sub_category_page_link,
                callback=self.parase_sub_category,
                cb_kwargs={"parent_category_name": category_name},
            )

    def parase_sub_category(self, response, parent_category_name):
        sub_catagories = response.xpath(
            "//h3[contains(text(),'Book Sub-Categories')]\
                                    /following-sibling::ul//a"
        )

        if sub_catagories:
            for sub_category in sub_catagories:
                loader = SubCategoryItemLoader(
                    item=SubCategoryItem(), selector=sub_category
                )
                loader.add_value("parent_category_name", parent_category_name)
                loader.add_css("sub_category_name", "::text")

                sub_category_items = loader.load_item()
                yield sub_category_items
