# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
import time
import os
def hello(request):
    if request.method != 'POST':
        return HttpResponse("only accept post method!")
    data = json.loads(request.body)
    now_time = unicode(time.time())
    file_name = u'./SourceData/' + data[u'file_name'] + u"_" + now_time
    sfname = os.path.abspath(file_name)
    file_name = u'./ResultData/' + data[u'file_name'] + u"_result_" + now_time
    rfname = os.path.abspath(file_name)
    cat_id_list = data[u'cat_id_list']
    email = data[u'email']
    with open(sfname, "w") as f:
        for cat_id in cat_id_list:
            f.write(cat_id + u'\n')
    start_scrapy(sfname, rfname, email)
    return HttpResponse("success!")
def start_scrapy(sfname, rfname, email):
    scrapy_path = os.path.dirname(sfname) + "/../Scrapy/Taobao"
    os.system("cd %s;nohup scrapy crawl taobao -a sfname='%s' -a rfname='%s' -a email='%s' &" % (scrapy_path, sfname, rfname, email))
    
    
    