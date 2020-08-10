#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import re_path
from firstapp import views

urlpatterns = [
    re_path('add_book$', views.add_book),
    re_path('show_books/', views.show_books),
]