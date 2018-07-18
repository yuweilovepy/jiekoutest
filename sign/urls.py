# -*- coding:utf-8 -*-

from django.conf.urls import url
from sign import views_if

urlpatterns = [
    # sign system interface
    #ex:/api/add_event
    url(r'^add_event/',views_if.add_event,name='add_event'),
    #ex:/api/get_event_list/
    url(r'^get_event_list/',views_if.get_event_list,name='get_event_list'),
    #ex:/api/add_guest/
    url(r'^add_guest/',views_if.add_guest,name='add_guest')

]