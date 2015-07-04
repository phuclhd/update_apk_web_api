# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from myproject.myapp.views import api
urlpatterns = patterns('myproject.myapp.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^api/$', api),
)
