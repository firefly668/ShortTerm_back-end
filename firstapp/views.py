from django.shortcuts import render
from django.db.models import Avg, Max, Min, Sum
from firstapp.models import User
from firstapp.models import Permission
from firstapp.models import Document
from firstapp.models import Team
from firstapp.models import Document_through_CollectUser
from firstapp.models import Document_through_BrowseUser
from firstapp.models import Document_through_EditUser
from firstapp.models import User_through_Team
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
import json
import random
import datetime

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
                auth_user = User.objects.get(pk=auth.User.pk)
                auth_user_name = auth_user.User_name
                teamer_auth['name'] =auth_user_name
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
        data = json.loads(request.body)
        teamername = data['teamername']
        aid = data['aid']
        tid = data['tid']
        if tid and aid and teamername:
            for teamer in teamername:
                user = User.objects.get(User_name=teamer['name'])
                if user:
                    permission = Permission.objects.get(Team=tid,Document=aid,User=user.pk)
                    if permission:
                        for auth in teamer['authority']:

                            if auth==1:
                                permission.one =True
                                permission.save()
                                continue
                            else:
                                permission.one = False

                            if auth==2:
                                permission.two =True
                                permission.save()
                                continue
                            else:
                                permission.two = False

                            if auth==3:
                                permission.three =True
                                permission.save()
                                continue
                            else:
                                permission.three = False

                            if auth==4:
                                permission.four =True
                                permission.save()
                                continue
                            else:
                                permission.four = False

                            if auth==5:
                                permission.five =True
                                permission.save()
                                continue
                            else:
                                permission.five = False
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
            respose['teamername']=teamername
            respose['aid']=aid
            respose['tid']=tid
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
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                respose['validation']=False
                return JsonResponse(respose)
            try:
                user_email = request.POST.get('email')
                if user_email:
                    captcha = request.POST.get('captcha')
                    if captcha:
                        captcha = int(captcha)
                        user.User_email= user_email
                        user.save()

                user_name = request.POST.get('username')
                if user_name:
                    user.User_name = user_name
                    user.save()

                new_password = request.POST.get('new_password')
                if new_password:
                    user.password = new_password
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

def checkPassword(request):
    respose={}
    if request.method=="POST":
        old_password = request.POST.get('old_password')
        UID = request.POST.get('UID')
        if UID:
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                respose['validation']=False
                return JsonResponse(respose)
            if old_password:
                if old_password==user.password:
                    respose['validation']=True
                    return  JsonResponse(respose)
                else:
                    respose['validation'] = False
                    return JsonResponse(respose)
            else:
                respose['validation'] = False
                return JsonResponse(respose)
        else:
            respose['validation'] = False
            return JsonResponse(respose)

def checkTeamName(request):
    respose={}
    if request.method == "POST":
        teamName = request.POST.get('teamName')
        teamOwner = request.POST.get('teamOwner')
        if teamName and teamOwner:
            team = Team.objects.filter(team_name=teamName,creater_id=teamOwner)
            if team:
                respose['isExist']=False
            else:
                respose['isExist']=True
        else:
            respose['isExist']=False
        return JsonResponse(respose)

def checkTeam(request):
    respose = {}
    if request.method == "POST":
        teamName = request.POST.get('teamName')
        teamOwner = request.POST.get('teamOwner')
        if teamName and teamOwner:
            team = Team()
            team.team_name=teamName
            team.creater_id=teamOwner
            team.save()
            User_through_Team.objects.create(User_id=teamOwner,Team=team)
            respose['status']=True
            respose['teamName']=teamName
            respose['teamOwner']=teamOwner
            respose['TID']=team.pk
        else:
            respose['status'] = False
        return JsonResponse(respose)

def sendMyArticle(request):
    respose={}
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        Content = request.POST.get('Content')
        Title = request.POST.get('Title')
        if UID and AID and Content and Title:
            if TID:
                UID = int(UID)
                AID = int(AID)
                TID = int(TID)
                if AID == -1:
                    try:
                        document = Document()
                        document.title = Title
                        document.content = Content
                        document.User = User.objects.get(pk=UID)
                        document.Team_id = TID
                        document.save()
                        Permission.objects.create(Team_id=TID,Document=document,User_id=UID)
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                else:
                    try:
                        document = Document.objects.get(pk=AID)
                        document.title = Title
                        document.content = Content
                        document.User = User.objects.get(pk=UID)
                        document.Team_id = TID
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)

                respose['Status'] = True
                return JsonResponse(respose)
            else:
                UID = int(UID)
                AID = int(AID)
                if AID == -1:
                    try:
                        document = Document()
                        document.title = Title
                        document.content=Content
                        document.User=User.objects.get(pk=UID)
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                else:
                    try:
                        document = Document.objects.get(pk=AID)
                        document.title = Title
                        document.content = Content
                        document.User = User.objects.get(pk=UID)
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)

                respose['Status']=True
                return JsonResponse(respose)
        else:
            respose['Status']=False
            respose['UID']=UID
            respose['AID']=AID
            respose['Content']=Content
            respose['Title']=Title
            return JsonResponse(respose)

def sendMyModel(request):
    respose = {}
    if request.method == "POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        Content = request.POST.get('Content')
        Title = request.POST.get('Title')
        if UID and AID and Content and Title:
            if TID:
                AID = int(AID)
                UID = int(UID)
                TID = int(TID)
                if AID == -1:
                    try:
                        document = Document()
                        document.title = Title
                        document.content = Content
                        document.model = True
                        document.User = User.objects.get(pk=UID)
                        document.Team_id = TID
                        document.save()
                        Permission.objects.create(Team_id=TID,Document=document,User_id=UID)
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                else:
                    try:
                        document = Document.objects.get(pk=AID)
                        document.title = Title
                        document.content = Content
                        document.model = True
                        document.User = User.objects.get(pk=UID)
                        document.Team_id = TID
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                respose['Status'] = True
                return JsonResponse(respose)
            else:
                AID = int(AID)
                UID = int(UID)
                if AID == -1:
                    try:
                        document = Document()
                        document.title = Title
                        document.content = Content
                        document.model=True
                        document.User = User.objects.get(pk=UID)
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                else:
                    try:
                        document = Document.objects.get(pk=AID)
                        document.title = Title
                        document.content = Content
                        document.model=True
                        document.User = User.objects.get(pk=UID)
                        document.save()
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    except Exception as e:
                        respose['Status'] = False
                        respose['UID'] = UID
                        respose['AID'] = AID
                        respose['TID'] = TID
                        respose['Content'] = Content
                        respose['Title'] = Title
                        return JsonResponse(respose)
                respose['Status'] = True
                return JsonResponse(respose)
        else:
            respose['Status'] = False
            respose['UID'] = UID
            respose['AID'] = AID
            respose['Content'] = Content
            respose['Title'] = Title
            return JsonResponse(respose)

def getArticle(request):
    respose={}
    if request.method=="POST":
        AID = request.POST.get('AID')
        UID = request.POST.get('UID')
        if AID and UID:
            AID = int(AID)
            UID = int(UID)
            try:
                document = Document.objects.get(pk=AID)
                dtb = Document_through_BrowseUser()
                dtb.Document=document
                dtb.User_id=UID
                dtb.save()
                respose['Status'] = True
                respose['Content'] = document.content
                respose['Title'] = document.title
                return JsonResponse(respose)
            except Exception as e:
                respose['Status']=False
                respose['Content']=""
                respose['Title']=""
                return JsonResponse(respose)
        else:
            respose['Status'] = False
            respose['Content'] = ""
            respose['Title'] = ""
            return JsonResponse(respose)

def someInfo(request):
    respose={}
    respose['myTeam']=[]
    respose['Documents1']=[]
    respose['Documents2']=[]
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            UID = int(UID)
            respose['UID']=UID
            teams = User_through_Team.objects.filter(User_id=UID)
            if teams:
                for team in teams:
                    try:
                        t = {}
                        tm = Team.objects.get(pk=team.Team_id)
                        t['TID']=tm.pk
                        t['TeamName']=tm.team_name
                        respose['myTeam'].append(t)
                    except Exception as e:
                        print(e)

            documents1_B = Document_through_BrowseUser.objects.filter(User_id=UID,Browse_time__gte=(datetime.datetime.today() - datetime.timedelta(7)))
            if documents1_B:
                for documents1 in documents1_B:
                    try:
                        d = {}
                        document = Document.objects.get(pk=documents1.Document_id)
                        d['lastEditDate']=document.last_time
                        d['documentName']=document.title
                        d['documentOwner']=document.User_id
                        respose['Documents1'].append(d)
                    except Exception as e:
                        print(e)

            documents2 = Document_through_EditUser.objects.filter(User_id=UID,Edit_time__gte=(datetime.datetime.today() - datetime.timedelta(7)))
            if documents2:
                for document in documents2:
                    try:
                        d = {}
                        dt = Document.objects.get(pk=document.Document_id)
                        d['lastEditDate'] = dt.last_time
                        d['documentName'] = dt.title
                        d['documentOwner'] = dt.User_id
                        respose['Documents2'].append(d)
                    except Exception as e:
                        print(e)
        return JsonResponse(respose)

def teamList(request):
    respose={}
    respose['Status']=False
    respose['teams']=[]
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            UID = int(UID)
            teams = User_through_Team.objects.filter(User_id=UID)
            for team in teams:
                try:
                    t={}
                    tm = Team.objects.get(pk=team.Team_id)
                    t['TID']=tm.pk
                    t['TeamName']=tm.team_name
                    respose['teams'].append(t)
                except Exception as e:
                    print(e)
                    return JsonResponse(respose)
            respose['Status']=True
        return  JsonResponse(respose)





