# -*- coding: utf-8 -*-

# import datetime
# import logging
# import scrapy
#
# from scrapy import Request
#
# from sourcelisting.models import SourceUrl
# from sourcelisting import spider
# from ..items import SourceUrlItem
#
# logger = logging.getLogger(__name__)
#
#
# class SourceUrlSpider(scrapy.Spider):
#     name = 'source_url_spider'
#     start_time = datetime.datetime.now()
#
#     def __init__(self, *args, **kwargs):
#         self.item_count = 0
#         super(SourceUrlSpider, self).__init__(*args, **kwargs)
#
#     def start_requests(self):
#         source_url_qs = SourceUrl.objects.all()
#         if source_url_qs:
#             self.item_count = source_url_qs.count()
#             logger.info("{} item procesed".format(self.item_count))
#
#             for index, source_url_obj in enumerate(source_url_qs):
#                 url = source_url_obj.url
#                 logger.info(
#                     "{}  {} Processing Source Url {}".format(
#                         index+1, source_url_obj.id, url)
#                 )
#
#                 yield Request(
#                     url,
#                     self.parse_page,
#                     errorback= self.request_handler,
#                     meta={
#                         'source_url_obj': source_url_obj
#                     }
#                 )
#         else:
#             logger.info("SourceURLQS is empty")
#
#     def parse_page(self, response):
#         source_url_obj = response.meta['source_url_obj']
#         html_body = response.body()
#         custom_parser = spider()
#         try:
#             tag_value = custom_parser(html_body, tag_name=source_url_obj.tag_name,
#                           tag_attr= source_url_obj.tag_attr,
#                           tag_attr_value= source_url_obj.tag_value
#                           )
#             snapshot = custom_parser.get_text(tag_value)
#         except Exception as e:
#             logger.info(
#                 "Tag Value Not Found {} {} Error {}".format(
#                     source_url_obj.id,source_url_obj.url, e)
#             )
#             snapshot = ''
#         item = SourceUrlItem()
#         item['snapshot'] = snapshot
#         item['source_url_obj'] = source_url_obj
#         yield item
#
#     def request_handler(self, failure):
#         logger.info("Error {}".format(failure))











