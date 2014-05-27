# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CarzoneItem(Item):
    title = Field()
    link = Field()
    carYear = Field()
    location = Field()
    mileage = Field()
    engine = Field()
    price = Field()
    Transmission = Field()
    Colour = Field()
    Owners = Field()
    NCT = Field()
    BodyType = Field()


