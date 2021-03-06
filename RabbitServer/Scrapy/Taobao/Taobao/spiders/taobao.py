#-*- coding:utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from Taobao.items import TaobaoItem
import codecs
import re

class TaobaoPySpider(BaseSpider):
    name = "taobao"
    id_pattern = re.compile("(\&|\?)id=(\d+)")
    get_page_num_failed_file_name = name + "_get_page_num_failed_url"
    get_page_failed_file_name = name + "_get_page_failed_url"
    result_file_name = name + "_entity.csv"
    
    def __init__(self, sfname, rfname, email):
        self.read_query_file_name = sfname
        self.result_file_name = rfname
        self.email = email
        super(TaobaoPySpider, self).__init__()
    
    def start_requests(self):
        rq_list = []
        with codecs.open(self.result_file_name, "w", encoding="GB18030") as f:
            f.write(u"cat_id" + u"," + u"title" + u"," + u"product_id" + u"\n")
        with open(self.read_query_file_name) as f:
            for line in f:
                url = "http://s.taobao.com/search?cat=%s&bcoffset=1&s=%s&n=100&style=grid" % (line.split('\t')[0].strip(), 0)
                rq_list.append(Request(url, meta={"cat_id": line.split('\t')[0].strip(), "get_page_num_failed_time": 0, "get_page_failed_time": 0}, dont_filter=True))
        return rq_list
        
    #获取页面总数
    def parse(self, response):
        meta_data = response.meta
        hxs = HtmlXPathSelector(response)
        page_info = hxs.select(u"//span[@class='page-info']/text()").extract()
        title_list = hxs.select("//h3[@class='summary']/a/@title").extract()
        total_page = 0
        try:
            total_page = int(page_info[0].split(u"/")[-1])
        except:
            #抓取失败，重新抓取
            if title_list:
                yield Request(response.url, callback=self.parse_1, meta=meta_data, dont_filter=True)
                return
            if meta_data[u'get_page_num_failed_time'] < 2:
                meta_data[u'get_page_num_failed_time'] += 1
                #设定延时抓取
                yield Request(response.url, callback=self.parse, meta=meta_data, dont_filter=True, priority=meta_data[u'get_page_num_failed_time'] + 2)
                return
            else:
                with open(self.get_page_num_failed_file_name, "a+") as f:
                    f.write(response.url + "\n")
                total_page = 0
            
        for i in range(0, total_page):
            num = "&s=%s&" % (i*40)
            url = response.url.replace("&s=0&", num)
            yield Request(url, callback=self.parse_1, meta=meta_data, dont_filter=True)
            

    def get_id(self, url):
        try:
            return self.id_pattern.search(url).group(2)
        except:
            return None
    
            
    def parse_1(self, response):
        meta_data = response.meta
        cat_id = meta_data['cat_id']
        hxs = HtmlXPathSelector(response)
        title_list = hxs.select("//h3[@class='summary']/a/@title").extract()
        href_list = hxs.select("//h3[@class='summary']/a/@href").extract()
        id_list = map(self.get_id, href_list)
        if not title_list or not id_list:
            if meta_data[u'get_page_failed_time'] < 2:
                meta_data[u'get_page_failed_time'] +=1
                yield Request(response.url, callback=self.parse_1, meta=meta_data, dont_filter=True, priority=meta_data[u'get_page_failed_time'] + 2)
                return
            else:
                with open(self.get_page_failed_file_name, "a+") as f:
                    f.write(response.url + "\n")
                    
        for title, product_id in zip(title_list, id_list):
            item = TaobaoItem()
            if cat_id:
                item['cat_id'] = cat_id
            else:
                item['cat_id'] = u"None"
            if title:
                item['title'] = title
            else:
                item['title'] = u"None"
            if product_id:
                item['product_id'] = product_id
            else:
                item['product_id'] = u"None"
            yield item
        
