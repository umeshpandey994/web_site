# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import logging


logger = logging.getLogger(__name__)


class SourceUrlPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'SourceUrlSpider':
            snapshot = item.get('snapshot')
            source_url_obj = item.get('source_url_obj')
            if snapshot:
                source_url_obj.new_snapshot = snapshot
                source_url_obj.last_triaged = datetime.datetime.now()
                source_url_obj.save()
            else:
                logger.info("snapshot is empty {}".format(source_url_obj))

