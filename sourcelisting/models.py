# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from subscribers.models import Company
import urllib


class Source(models.Model):
    created_by = models.ForeignKey(User, related_name="source_created")
    updated_by = models.ForeignKey(User, related_name="source_updated",
                                   default=28)
    companies = models.ManyToManyField(Company)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = (("url", "created_by"),)

    def aid_link(self):
        story_parms = {
            'source': self.id
        }
        encoded_params = urllib.urlencode(story_parms)
        popup = """<b><a href='#' onclick="return popitup('/admin/stories/story/add/?{}', '{}')">{}</a></b>""".format(encoded_params, self.url, self.name)
        return popup


    aid_link.allow_tags = True
    #aid_link.admin_order_field = 'name'

    def test_popup(self):
        return """
            <a href="{}" 
                target="popup" 
                onclick="window.open('{}','popup','width=600,height=600'); return false;  window.open('http://kanishkkunal.in','popup','width=600,height=600'); return false;">
                Open Link in Popup
            </a>
        """.format(self.url, self.url)
    test_popup.allow_tags = True