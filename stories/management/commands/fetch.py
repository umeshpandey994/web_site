from django.core.management.base import BaseCommand, CommandError

from sourcelisting.models import Source
from sourcelisting.views import fetchstory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sourceid', dest="sourceid", nargs="?", type=int)
        parser.add_argument('--sourcelist', dest="sourcelist", nargs="+",
                            type=int)
        parser.add_argument('--userid', dest="userid", nargs="?", type=int)

    def handle(self, *args, **options):
        if options.get('sourceid'):
            f = options['sourceid']
            fetchstory(int(f))
        elif options.get('sourcelist'):
            li = options['sourcelist']
            for i in li:
                fetchstory(int(i))
        elif options.get('userid'):
            userid = options['userid']
            source = Source.objects.filter(created_by=userid)
            for i in source:
                fetchstory(i.id)
        else:
            print "working"
            source = Source.objects.filter(created_by__is_active=True)
            for i in source:
                    fetchstory(i.id)
        return self.stdout.write(
                    self.style.SUCCESS('Sucessfully updated')
                )


