from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector

import datetime
import logging
import scrapy

logger = logging.getLogger(__name__)

_result_items_xpath = '//li[@class="g"]|//div[@class="g"]'
_title_rel_xpath = './/h3/a/descendant-or-self::*/text()'
_lead_rel_xpath = (
    '//*[@id="rso"]/li[1]/div/div/div[2]|.//div[@class="st"]/text()'
)

class RSSSpider(scrapy.Spider):
    name = 'RSSspider'
    start_time = datetime.datetime.now()

    def __init__(self, *args, **kwargs):
        self.item_count = 0
        super(RSSSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = [
            u'https://www.google.com/search?authuser=0&tbs=qdr%3Aw%2Ccd_max%3A2017%2F12%2F19%2Ccd_min%3A2017%2F12%2F18&q=intext%3A%28%28Deloitte%29+AND+%28%22Base+Erosion+and+Profit+Shifting%22+OR+%22BEPS%22+OR+%22Multinational+Anti-Avoidance+Law%22+OR+%22Tax+controversy%22+OR+%22Managed+investment+trusts%22+OR+%22Tax+Technology%22%29%29&start=0&num=100&tbm=nws&hl=en&lr=lang_en&gl=in'
        ]
        for indx, i in enumerate(url):
                yield Request(
                        i,
                        self.parse_page,
                        errback=self.request_error_handler
                )

    def parse_page(self, response):
        item = []
        try:
            for sel in response.xpath(_result_items_xpath):
                item.append(''.join(sel.xpath(_title_rel_xpath).extract()))
                item.append(''.join(sel.xpath(_lead_rel_xpath).extract()))
            print item
        except Exception as e:
            print e

    def request_error_handler(self, failure):
        url = failure.request.url
        message = repr(failure.value) + ': ' + url
        print "5635463546456546565465645"
        print "##########################"
        print url
        print message
