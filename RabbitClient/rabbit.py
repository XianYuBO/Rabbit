#!/urs/bin/python
# -*- coding:utf-8 -*-

import settings
import codecs
import os
import re
import requests
import json

class Rabbit(object):

    def __init__(self):
        self.data_path = settings.data_path
        self.email = settings.email
        self.url = settings.url
        self.data = {}
        self.init_check()
        self.upload_file()
        
    def init_check(self):
        print "...check file...Doing"
        if not os.path.isfile(self.data_path):
            print "The source file is not existed!"
            exit(-1)
        print "...file exists...Done"
        self.data.update({"file_name" : os.path.basename(self.data_path)})
        cat_id_list = []
        with codecs.open(self.data_path) as f:
            for line in f:
                cat_id = line.split(u'\t')[0].strip()
                if not re.findall('^\d+$', cat_id):
                    print "The source file is illegal!"
                    exit(0)
                else:
                    cat_id_list.append(cat_id)
        self.data.update({"cat_id_list" : cat_id_list, "email" : self.email})
        print "...file is valid...Done"
        print "...check file...Done"

    def upload_file(self):
        if self.data:
            data = json.dumps(self.data)
        else:
            print "No urls will be posted!"
            exit(0)
        headers = {'enctype' : "multipart/form-data"}
        r = requests.post(self.url, data=data, headers=headers)
        if r.status_code == 200:
            print "upload file successfully!"
        else:
            print "fail to upload file!"
        
if __name__ == '__main__':
    rabbit = Rabbit()
    
