from django.conf.urls import patterns,url
from ResultScrap import views

urlpatterns = patterns("",
    url(r'^$', views.homepage, name="homepage"),
    url(r'^ResultPage/$', views.result_page, name="result_page"),
)
