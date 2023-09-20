from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst,MapCompose

class CategoryItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    category_name_in = MapCompose(lambda name: name.strip())


class SubCategoryItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    parent_category_name_in = MapCompose(lambda name: name.strip())
    sub_category_name_in = MapCompose(lambda name: name.strip())