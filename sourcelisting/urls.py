from django.conf.urls import url
from sourcelisting import views

urlpatterns = [

    url(r'^add/$', views.add_source),
    url(r'^delete/(?P<del_id>\d+)$', views.delete_source),
    url(r'^edit/(?P<edit_id>\d+)/$', views.edit_source),
    url(r'^fetch_stories/(?P<id>\d+)/$', views.fetch_stories),
    url(r'^listing/$', views.listing),
    url(r'^search_source/$', views.search_source),
    url(r'^fetchall/$', views.fetchall),


]