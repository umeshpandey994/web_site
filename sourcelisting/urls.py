from django.conf.urls import url
from sourcelisting import views

urlpatterns = [

    url(r'^add/$', views.add),
    url(r'^delete/(?P<del_id>\d+)$', views.delete),
    url(r'^edit/(?P<edit_id>\d+)/$', views.edit),
    url(r'^fetch_stories/(?P<id>\d+)/$', views.fetch_stories)


]