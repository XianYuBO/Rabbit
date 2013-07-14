# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TaobaoItem(Item):
    # define the fields for your item here like:
    cat_id = Field()
    title = Field()
    product_id = Field()
