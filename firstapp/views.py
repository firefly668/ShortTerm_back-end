from django.shortcuts import render
from firstapp.models import User
from firstapp.models import Permission
from firstapp.models import Document
from firstapp.models import Team
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
import json
import random

# Create your views here.
def checkUsername(request):
    respose={}
    if request.method=="POST":
        Username = request.POST.get('Username')
        user = User.objects.filter(User_name=Username)
        if user:
            respose['Used']=True
        else:
            respose['Used']=False
        return JsonResponse(respose)

def checkEmail(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        user = User.objects.filter(User_email=Email)
        if user:
            respose['Used']=True
        else:
            respose['Used']=False
        return JsonResponse(respose)

def captcha(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        number = random.randint(100000,999999)
        try:
            send_mail('金刚石注册验证',"您的验证码为：" + str(number) + "请尽快完成验证",'1205672770@qq.com',[Email])
            respose['Status']=True
            request.session['checknumber']=number
        except Exception as e:
            respose['Status']=False
        return JsonResponse(respose)

def register(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        Captcha = int(request.POST.get('Captcha'))
        if Captcha==request.session.get('checknumber',default=None):
            new_user = User()
            new_user.password=Password
            new_user.User_email=Email
            new_user.User_name=Username
            new_user.save()
            user = User.objects.filter(User_email=Email)
            respose['UserId']=user[0].pk
            respose['Username']=user[0].User_name
            if user[0].avatar:
                respose['AvatarUrl']=user[0].avatar.path
            else:
                respose['AvatarUrl']=""
            respose['Status']=True
        else:
            respose['Status']=False
        return JsonResponse(respose)

def login(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        user = User.objects.filter(User_email=Email).filter(password=Password)
        if user:
            request.session['is_login']=True
            request.session['user_id']=user[0].pk
            respose['UserId']=user[0].pk
            if user[0].avatar:
                respose['AvatarUrl'] = user[0].avatar.path
            else:
                respose['AvatarUrl'] = ""
            respose['Username'] = user[0].User_name
            respose['Status']=True
        else:
            respose['Status']=False
        return JsonResponse(respose)

def getauthority(request):
    respose={}
    if request.method=="POST":
        tid = request.POST.get('tid')
        aid = request.POST.get('aid')
        if tid and aid:
            try:
                team = Team.objects.get(pk=tid)
                respose['name']=team.team_name
                respose['teamername']=[]
            except Exception as e:
                return JsonResponse(respose)
            authorities = Permission.objects.filter(Team=tid,Document=aid)
            for auth in authorities:
                teamer_auth = {}
                teamer_auth['name']=User.objects.get(pk=auth.User).User_name
                authority = []
                if auth.one:
                    authority.append(1)
                if auth.two:
                    authority.append(2)
                if auth.three:
                    authority.append(3)
                if auth.four:
                    authority.append(4)
                if auth.five:
                    authority.append(5)
                teamer_auth['authority']=authority
                respose['teamername'].append(teamer_auth)
        return  JsonResponse(respose)

def pushauthority(request):
    respose={}
    if request.method=="POST":
        tid = request.POST.get('tid')
        aid = request.POST.get('aid')
        teamername = request.POST.get('teamername')
        if tid and aid and len(teamername)>0:
            for teamer in teamername:
                user = User.objects.get(User_name=teamer['name'])
                if user:
                    permission = Permission.objects.filter(Team=tid,Document=aid,User=user.pk)
                    if permission:
                        for auth in teamer['authority']:
                            if auth==1:
                                permission.one =True
                                continue
                            else:
                                permission.one = False
                            if auth==2:
                                permission.two =True
                                continue
                            else:
                                permission.two = False
                            if auth==3:
                                permission.three =True
                                continue
                            else:
                                permission.three = False
                            if auth==4:
                                permission.four =True
                                continue
                            else:
                                permission.four = False
                            if auth==5:
                                permission.five =True
                                continue
                            else:
                                permission.five = False
                        permission.save()
                    else:
                        respose['feedback']=False
                        return JsonResponse(respose)
                else:
                    respose['feedback'] = False
                    return JsonResponse(respose)
            respose['feedback'] = True
            return JsonResponse(respose)
        else:
            respose['feedback'] = False
            return JsonResponse(respose)

def PersonIndex(request):
    respose={}
    if request.method=="POST":
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                respose['Username']=user.User_name
                respose['Email']=user.User_email
                return JsonResponse(respose)
            except Exception as e:
                respose['validation']=False
                return JsonResponse(respose)
        else:
            respose['validation'] = False
            return JsonResponse(respose)


def changeInfo(request):
    respose={}
    if request.method == "POST":
        UID = request.POST.get('UID')
        if UID:
            captcha = int(request.POST.get('captcha'))
            old_password = request.POST.get('old_password')
            user = User.objects.get(pk=UID)
            if captcha == request.session.get('captcha',None) and old_password==user.password:
                try:
                    user.User_email=request.POST.get('email')
                    user.User_name=request.POST.get('username')
                    user.password=request.POST.get('new_password')
                    user.save()
                    respose['validation']=True
                    respose['username_new']=user.User_name
                    respose['email_new']=user.User_email
                    return JsonResponse(respose)
                except Exception as e:
                    respose['validation']=False
                    return JsonResponse(respose)
            else:
                respose['validation'] = False
                return JsonResponse(respose)
        else:
            respose['validation'] = False
            return JsonResponse(respose)


