from django.core.management.base import BaseCommand, CommandError

from stories.models import Story
from sourcelisting.models import Source

from dateutil.parser import parse
from optparse import make_option
import feedparser

import requests
import re


def filterdata(data):
    p = re.compile(r'<.+>')
    return p.sub('', data)


def fetch(source_id):
    source = Source.objects.get(id=source_id)
    f = feedparser.parse(source.url)
    for entry in f.entries:
        if Story.objects.filter(url__exact=entry.link, source=source_id).exists():
            pass
        else:
            s = Story()
            s.url = entry.link
            s.title = entry.title
            dt = parse(str(entry.published))
            s.pub_date = dt
            s.body_text = filterdata(entry.summary)
            s.source_id = id
            s.client_id = source.created_by.subscriber_user.client_id
            s.save()
            list_companies = source.companies.values_list('id', flat=True)
            story_obj = Story.objects.get(id=s.id)
            story_obj.company.add(*list_companies)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('num', nargs="+", type=int)

    def handle(self, *args, **options):
        f = options.get('num')
        for i in f:
            print type(f)
            fetch(f)
        return self.stdout.write(
                    self.style.SUCCESS('Sucessfully updated')
                )


