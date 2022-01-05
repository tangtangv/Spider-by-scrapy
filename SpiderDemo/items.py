# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderdemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MaoyanreyingItem(scrapy.Item):
    ranking = scrapy.Field()  #排名
    title = scrapy.Field() #电影名
    star = scrapy.Field()  #主演
    releasetime = scrapy.Field() #上映时间
    score = scrapy.Field() #评分

class ScrapyredisproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    b_cate = scrapy.Field()
    m_cate = scrapy.Field()
    s_href = scrapy.Field()
    s_cate = scrapy.Field()
    book_img = scrapy.Field()
    book_name = scrapy.Field()
    book_desc = scrapy.Field()
    book_price = scrapy.Field()
    book_author = scrapy.Field()
    book_publish_date = scrapy.Field()
    book_press = scrapy.Field()



