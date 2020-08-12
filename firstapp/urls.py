#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import re_path
from django.urls import path
from firstapp import views

urlpatterns = [
    path('checkUsername/',views.checkUsername,name='checkUsername'),
    path('checkEmail/',views.checkEmail,name='checkEmail'),
    path('captcha/',views.captcha,name='captcha'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('getauthority/', views.getauthority, name='getauthority'),
    path('pushauthority/', views.pushauthority, name='pushauthority'),
    path('PersonIndex/',views.PersonIndex,name='PersonIndex'),
    path('changeInfo/', views.changeInfo, name='changeInfo'),
    path('sendMyArticle/', views.sendMyArticle, name='sendMyArticle'),
    path('sendMyModel/', views.sendMyModel, name='sendMyModel'),
    path('checkTeamName/', views.checkTeamName, name='checkTeamName'),
    path('checkTeam/', views.checkTeam, name='checkTeam'),
    path('checkPassword/',views.checkPassword,name='checkPassword'),
    path('checkTeamName/', views.checkTeamName, name='checkTeamName'),
    path('checkTeam/', views.checkTeam, name='checkTeam'),
    path('getArticle/', views.getArticle, name='getArticle'),
    path('someInfo/', views.someInfo, name='someInfo'),
    path('teamList/', views.teamList, name='teamList'),
]