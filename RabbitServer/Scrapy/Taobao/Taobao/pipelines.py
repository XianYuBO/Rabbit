# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import codecs
import re
import os
from scrapy.mail import MailSender

class TaobaoPipeline(object):
    def process_item(self, item, spider):
        with codecs.open(spider.result_file_name, "a+", encoding="GB18030") as f:
            f.write(item[u"cat_id"] + u"," + item[u"title"] + u"," + item[u"product_id"] + u"\n")
        return item
    def close_spider(self, spider):
        mailer = MailSender(mailfrom='xianyubo@baidu.com')
        name = "Rabbit user"
        try:
            name = re.search("(.+)@", spider.email).group(1)
        except:
            name = "Rabbit user"
        body = \
        """Dear %s:
               Hi! Your task %s is done.
               The result's path is %s.
               Thanks for using Rabbit system.
               If you have some advice or problems, you can contact with me by xianyubo@baidu.com or xianyubo@qq.com.
        """ % (name, os.path.basename(spider.read_query_file_name), os.path.basename(spider.result_file_name))
        with open(spider.result_file_name, "rb") as f:
            mailer.send(to=[spider.email], subject="Scrapy Taobao", body=body, attachs=[(os.path.basename(spider.result_file_name), "application/octet-stream", f)])
