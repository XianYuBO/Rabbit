# Scrapy settings for Taobao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'Taobao'

SPIDER_MODULES = ['Taobao.spiders']
NEWSPIDER_MODULE = 'Taobao.spiders'
DOWNLOAD_DELAY = 0.5
ITEM_PIPELINES = ['Taobao.pipelines.TaobaoPipeline']
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Taobao (+http://www.yourdomain.com)'
