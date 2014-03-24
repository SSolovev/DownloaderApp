__author__ = 'sergey'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url('^$', views.index, name='index'),
                       url('^result_link/$', views.get_link, name='get_link'),)

