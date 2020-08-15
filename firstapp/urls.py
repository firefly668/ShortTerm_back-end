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
    path('getauthority1/', views.getauthority1, name='getauthority1'),
    path('pushauthority1/', views.pushauthority1, name='pushauthority1'),
    path('getauthority2/', views.getauthority2, name='getauthority2'),
    path('pushauthority2/', views.pushauthority2, name='pushauthority2'),
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
    path('modifyRECD/', views.modifyRECD, name='modifyRECD'),
    path('memberList/', views.memberList, name='memberList'),
    path('kickMember/', views.kickMember, name='kickMember'),
    path('inviteMember/', views.inviteMember, name='inviteMember'),
    path('dismissTeam/', views.dismissTeam, name='dismissTeam'),
    path('deleteFile/', views.deleteFile, name='deleteFile'),
    path('collectFile/', views.collectFile, name='collectFile'),
    path('getUserAuthority/', views.getUserAuthority, name='getUserAuthority'),
    path('unCollectFile/', views.unCollectFile, name='unCollectFile'),
    path('CommentList/', views.CommentList, name='CommentList'),
    path('DeleteComment/', views.DeleteComment, name='DeleteComment'),
    path('NewComment/', views.NewComment, name='NewComment'),
    path('ReplyComment/', views.ReplyComment, name='ReplyComment'),
    path('myMessage/', views.myMessage, name='myMessage'),
    path('readMessage/', views.readMessage, name='readMessage'),
    path('replyInvitation/', views.replyInvitation, name='replyInvitation'),
    path('TeamInfo/', views.TeamInfo, name='TeamInfo'),

]