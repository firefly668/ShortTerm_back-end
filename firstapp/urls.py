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
    path('avatarUrl/', views.avatarUrl, name='avatarUrl'),
    path('picSave/', views.picSave, name='picSave'),
    path('authJudger/', views.authJudger, name='authJudger'),
    path('completeDeleteFile/', views.completeDeleteFile, name='completeDeleteFile'),
    path('restoreFile/', views.restoreFile, name='restoreFile'),
    path('quitTeam/', views.quitTeam, name='quitTeam'),
    path('someInfo1/', views.someInfo1, name='someInfo1'),
    path('someInfo2/', views.someInfo2, name='someInfo2'),
    path('changeTeamDescription/', views.changeTeamDescription, name='changeTeamDescription'),
    path('TeamInfo2/', views.TeamInfo2, name='TeamInfo2'),
    path('deleteMessage/', views.deleteMessage, name='deleteMessage'),
    path('AIDgetTID/', views.AIDgetTID, name='AIDgetTID'),
    path('getcheckNum/', views.getcheckNum, name='getcheckNum'),
    path('privateUpload/', views.privateUpload, name='privateUpload'),
    path('teamUpload/', views.teamUpload, name='teamUpload'),
    path('getTags/', views.getTags, name='getTags'),
    path('gototop/', views.gototop, name='gototop'),
    path('downloadFile/', views.downloadFile, name='downloadFile'),
    path('AIDtoUID/', views.AIDtoUID, name='AIDtoUID'),
    path('AIDgetMD5/', views.AIDgetMD5, name='AIDgetMD5'),
    path('isShared/', views.isShared, name='isShared'),

]
