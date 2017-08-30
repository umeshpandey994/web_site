from django.conf.urls import url
from subscribers import views


urlpatterns = [

    url(r'^login/$', views.user_login),
    url(r'^signup/$', views.signup),
    url(r'^someview/$', views.some_view)


]
