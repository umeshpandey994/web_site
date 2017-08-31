from django.conf.urls import url
from subscribers import views


urlpatterns = [

    url(r'^login/$', views.login_),
    url(r'^signup/$', views.signup),

]
