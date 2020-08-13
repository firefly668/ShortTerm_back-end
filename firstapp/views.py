from django.shortcuts import render
from django.db.models import Avg, Max, Min, Sum
from firstapp.models import User
from firstapp.models import Document
from firstapp.models import Team
from firstapp.models import Document_through_CollectUser
from firstapp.models import Document_through_BrowseUser
from firstapp.models import Document_through_EditUser
from firstapp.models import User_through_Team
from firstapp.models import Inviter_through_Team
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
import json
import simplejson
import random
import datetime

# Create your views here.
def checkUsername(request):
    response={}
    if request.method=="POST":
        Username = request.POST.get('Username')
        user = User.objects.filter(User_name=Username)
        if user:
            response['Used']=True
        else:
            response['Used']=False
        return JsonResponse(response)

def checkEmail(request):
    response={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        user = User.objects.filter(User_email=Email)
        if user:
            response['Used']=True
        else:
            response['Used']=False
        return JsonResponse(response)

def captcha(request):
    response={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        number = random.randint(100000,999999)
        try:
            send_mail('金刚石注册验证',"您的验证码为：" + str(number) + "请尽快完成验证",'1205672770@qq.com',[Email])
            response['Status']=True
            request.session['checknumber']=number
        except Exception as e:
            response['Status']=False
        return JsonResponse(response)

def register(request):
    response={}
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
            response['UserId']=user[0].pk
            response['Username']=user[0].User_name
            if user[0].avatar:
                response['AvatarUrl']=user[0].avatar.path
            else:
                response['AvatarUrl']=""
            response['Status']=True
        else:
            response['Status']=False
        return JsonResponse(response)

def login(request):
    response={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        user = User.objects.filter(User_email=Email).filter(password=Password)
        if user:
            request.session['is_login']=True
            request.session['user_id']=user[0].pk
            response['UserId']=user[0].pk
            if user[0].avatar:
                response['AvatarUrl'] = user[0].avatar.path
            else:
                response['AvatarUrl'] = ""
            response['Username'] = user[0].User_name
            response['Status']=True
        else:
            response['Status']=False
        return JsonResponse(response)

def getauthority1(request):
    response={}
    if request.method=="POST":
        AID = request.POST.get('aid')
        if AID:
            AID = int(AID)
            try:
                document = Document.objects.get(pk=AID)
                if document.Team:
                    response['Rnum'] = document.Rnum
                    response['Enum'] = document.Enum
                    response['Cnum'] = document.Cnum
                    response['Dnum'] = document.Dnum
                else:
                    response['error'] = "this document is not a team document"
                    return JsonResponse(response)
            except Exception as e:
                response['error']="can't find document"
                print(e)
        else:
            response['error']="aid wrong"
        return  JsonResponse(response)

def pushauthority1(request):
    response = {}
    response['feedback']=False
    if request.method == "POST":
        AID = request.POST.get('aid')
        Rnum = request.POST.get('Rnum')
        Enum = request.POST.get('Enum')
        Cnum = request.POST.get('Cnum')
        Dnum = request.POST.get('Dnum')
        if AID and Rnum and Enum and Dnum:
            AID = int(AID)
            Rnum = int(Rnum)
            Enum = int(Enum)
            Cnum = int(Cnum)
            Dnum = int(Dnum)
            try:
                document = Document.objects.get(pk=AID)
                if document.Team:
                    document.Rnum = Rnum
                    document.Enum = Enum
                    document.Cnum = Cnum
                    document.Dnum = Dnum
                    document.save()
                    response['feedback']=True
                else:
                    response['error'] = "this document is not a team document"
                    return JsonResponse(response)
            except Exception as e:
                response['error'] = "can't find document"
                print(e)
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def getauthority2(request):
    response = {}
    if request.method == "POST":
        AID = request.POST.get('aid')
        if AID:
            AID = int(AID)
            try:
                document = Document.objects.get(pk=AID)
                response['Rnum'] = document.readable
                response['Enum'] = document.editable
                response['Cnum'] = document.judgeable
                response['Dnum'] = document.deleteable
            except Exception as e:
                response['error'] = "can't find document"
                print(e)
        else:
            response['error'] = "aid wrong"
        return JsonResponse(response)

def pushauthority2(request):
    response = {}
    response['feedback']=False
    if request.method == "POST":
        AID = request.POST.get('aid')
        Rnum = request.POST.get('Rnum')
        Enum = request.POST.get('Enum')
        Cnum = request.POST.get('Cnum')
        Dnum = request.POST.get('Dnum')
        if AID:
            AID = int(AID)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                response['error'] = "can't find document"
                print(e)
                return JsonResponse(response)
            try:
                if Rnum == "true":
                    document.readable = True
                elif Rnum == "false":
                    document.readable = False

                if Enum == "true":
                    document.editable = True
                elif Enum == "false":
                    document.editable = False

                if Cnum == "true":
                    document.judgeable = True
                elif Cnum == "false":
                    document.judgeable = False

                if Dnum == "true":
                    document.deleteable = True
                elif Dnum == "false":
                    document.deleteable = False
                document.save()
                response['feedback']=True
            except Exception as e:
                response['error'] = "edit fail"
                print(e)
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def PersonIndex(request):
    response={}
    if request.method=="POST":
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                response['Username']=user.User_name
                response['Email']=user.User_email
                return JsonResponse(response)
            except Exception as e:
                response['validation']=False
                return JsonResponse(response)
        else:
            response['validation'] = False
            return JsonResponse(response)

def changeInfo(request):
    response={}
    if request.method == "POST":
        UID = request.POST.get('UID')
        if UID:
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['validation']=False
                return JsonResponse(response)
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

                response['validation']=True
                response['username_new']=user.User_name
                response['email_new']=user.User_email
                return JsonResponse(response)
            except Exception as e:
                response['validation']=False
                return JsonResponse(response)
        else:
            response['validation'] = False
            return JsonResponse(response)

def checkPassword(request):
    response={}
    if request.method=="POST":
        old_password = request.POST.get('old_password')
        UID = request.POST.get('UID')
        if UID:
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['validation']=False
                return JsonResponse(response)
            if old_password:
                if old_password==user.password:
                    response['validation']=True
                    return  JsonResponse(response)
                else:
                    response['validation'] = False
                    return JsonResponse(response)
            else:
                response['validation'] = False
                return JsonResponse(response)
        else:
            response['validation'] = False
            return JsonResponse(response)

def checkTeamName(request):
    response={}
    if request.method == "POST":
        teamName = request.POST.get('teamName')
        teamOwner = request.POST.get('teamOwner')
        if teamName and teamOwner:
            team = Team.objects.filter(team_name=teamName,creater_id=teamOwner)
            if team:
                response['isExist']=False
            else:
                response['isExist']=True
        else:
            response['isExist']=False
        return JsonResponse(response)

def checkTeam(request):
    response = {}
    if request.method == "POST":
        teamName = request.POST.get('teamName')
        teamOwner = request.POST.get('teamOwner')
        if teamName and teamOwner:
            team = Team()
            team.team_name=teamName
            team.creater_id=teamOwner
            team.save()
            User_through_Team.objects.create(User_id=teamOwner,Team=team,level=5)
            response['status']=True
            response['teamName']=teamName
            response['teamOwner']=teamOwner
            response['TID']=team.pk
        else:
            response['status'] = False
        return JsonResponse(response)

def sendMyArticle(request):
    response={}
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        Content = request.POST.get('Content')
        Title = request.POST.get('Title')
        if UID and AID and Content and Title:
            UID = int(UID)
            AID = int(AID)
            if AID == -1:
                try:
                    document = Document()
                    document.title = Title
                    document.content = Content
                    document.User = User.objects.get(pk=UID)
                    if TID:
                        document.Team_id = int(TID)
                    document.save()
                    response['AID']=document.pk
                    Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    Document_through_BrowseUser.objects.create(Document=document,User_id=UID)
                except Exception as e:
                    response['Status'] = False
                    response['UID'] = UID
                    response['AID'] = AID
                    response['TID'] = TID
                    response['Content'] = Content
                    response['Title'] = Title
                    return JsonResponse(response)
            else:
                try:
                    document = Document.objects.get(pk=AID)
                    document.title = Title
                    document.content = Content
                    if TID:
                        document.Team_id = int(TID)
                    document.save()
                    try:
                        dte = Document_through_EditUser.objects.get(Document=document,User_id=UID)
                        dte.Edit_time = datetime.datetime.now()
                    except Exception as e:
                        print(e)
                        Document_through_EditUser.objects.create(Document=document, User_id=UID)
                        response['warning']="last edition didn't record,but this time is done."
                except Exception as e:
                    response['Status'] = False
                    response['error'] = "AID wrong"
                    return JsonResponse(response)
            response['Status'] = True
            return JsonResponse(response)
        else:
            response['Status']=False
            response['error']="lost data"
            response['UID']=UID
            response['AID']=AID
            response['Content']=Content
            response['Title']=Title
            return JsonResponse(response)

def sendMyModel(request):
    response = {}
    if request.method == "POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        Content = request.POST.get('Content')
        Title = request.POST.get('Title')
        if UID and AID and Content and Title:
            AID = int(AID)
            UID = int(UID)
            if AID == -1:
                try:
                    document = Document()
                    document.title = Title
                    document.content = Content
                    document.model = True
                    document.User = User.objects.get(pk=UID)
                    if TID:
                        document.Team_id = int(TID)
                    document.save()
                    response['AID']=document.pk
                except Exception as e:
                    print(e)
                    response['error'] = "UID wrong"
                    response['Status'] = False
                    return JsonResponse(response)
            else:
                response['error']="AID!=-1"
                return JsonResponse(request)
            response['Status'] = True
            return JsonResponse(response)
        else:
            response['Status'] = False
            response['error'] = "lost data"
            response['UID'] = UID
            response['AID'] = AID
            response['Content'] = Content
            response['Title'] = Title
            return JsonResponse(response)

def getArticle(request):
    response={}
    if request.method=="POST":
        AID = request.POST.get('AID')
        UID = request.POST.get('UID')
        if AID and UID:
            AID = int(AID)
            UID = int(UID)
            try:
                document = Document.objects.get(pk=AID)
                try:
                    dtb = Document_through_BrowseUser.objects.get(Document=document,User_id=UID)
                    dtb.Browse_time = datetime.datetime.now()
                    dtb.save()
                except Exception as e:
                    print(e)
                    response['warning']="last browse didn't record,but this time is done."
                    dtb = Document_through_BrowseUser()
                    dtb.Document=document
                    dtb.User_id=UID
                    dtb.save()
                response['Status'] = True
                response['Content'] = document.content
                response['Title'] = document.title
                return JsonResponse(response)
            except Exception as e:
                response["error"]="AID wrong"
                response['Status']=False
                response['Content']=""
                response['Title']=""
                return JsonResponse(response)
        else:
            response['error'] = "lost data"
            response['Status'] = False
            response['Content'] = ""
            response['Title'] = ""
            return JsonResponse(response)

def someInfo(request):
    response={}
    response['myTeam']=[]
    response['Documents1']=[]
    response['Documents2']=[]
    response['Documents3']=[]
    response['Documents4']=[]
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            UID = int(UID)
            response['UID']=UID

            teams = User_through_Team.objects.filter(User_id=UID)
            if teams:
                for team in teams:
                    try:
                        t = {}
                        tm = Team.objects.get(pk=team.Team_id)
                        t['TID']=tm.pk
                        t['teamName']=tm.team_name
                        response['myTeam'].append(t)
                    except Exception as e:
                        print(e)

            documents1_B = Document_through_BrowseUser.objects.filter(User_id=UID,Browse_time__gte=(datetime.datetime.now() - datetime.timedelta(3)))
            if documents1_B:
                for documents1 in documents1_B:
                    try:
                        d = {}
                        document = Document.objects.get(pk=documents1.Document_id)
                        user = User.objects.get(pk=document.User_id)
                        d['lastEditDate']=document.last_time
                        d['documentName']=document.title
                        d['documentOwner']=user.User_name
                        d['AID']=document.pk
                        d['UID']=document.User_id
                        if document.Team:
                            d['TID']=document.Team_id
                        else:
                            d['TID']=""
                        response['Documents1'].append(d)
                    except Exception as e:
                        print(e)

            documents2 = Document_through_EditUser.objects.filter(User_id=UID,Edit_time__gte=(datetime.datetime.now() - datetime.timedelta(3)))
            if documents2:
                for document in documents2:
                    try:
                        d = {}
                        dt = Document.objects.get(pk=document.Document_id)
                        user = User.objects.get(pk=dt.User_id)
                        d['lastEditDate'] = dt.last_time
                        d['documentName'] = dt.title
                        d['documentOwner'] = user.User_name
                        d['AID']=dt.pk
                        d['UID']=dt.User_id
                        if dt.Team:
                            d['TID']=dt.Team_id
                        else:
                            d['TID']=""
                        response['Documents2'].append(d)
                    except Exception as e:
                        print(e)

            documents3 = Document_through_CollectUser.objects.filter(User_id=UID)
            if documents3:
                for document in documents3:
                    try:
                        d={}
                        dt = Document.objects.get(pk=document.Document_id)
                        user = User.objects.get(pk=dt.User_id)
                        d['lastEditDate'] = dt.last_time
                        d['documentName'] = dt.title
                        d['documentOwner'] = user.User_name
                        d['AID'] = dt.pk
                        d['UID'] = dt.User_id
                        if dt.Team:
                            d['TID']=dt.Team_id
                        else:
                            d['TID']=""
                        response['Documents3'].append(d)
                    except Exception as e:
                        print(e)

            documents4 = Document.objects.filter(User_id=UID,model=True)
            if documents4:
                for document in documents4:
                    if document.Team:
                        pass
                    else:
                        d={}
                        d['documentName']=document.title
                        d['UID']=document.User_id
                        d['MID']=document.pk
                        response['Documents4'].append(d)
        else:
            response['error']="lost data"
        return JsonResponse(response)

def teamList(request):
    response={}
    response['Status']=False
    response['teams']=[]
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
                    response['teams'].append(t)
                except Exception as e:
                    print(e)
                    return JsonResponse(response)
            response['Status']=True
        return  JsonResponse(response)

def modifyRECD(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        TID = request.POST.get('TID')
        UID = request.POST.get('UID')
        Level = request.POST.get('Level')
        if TID and UID and Level:
            try:
                utt = User_through_Team.objects.get(Team_id=TID,User_id=UID)
                utt.level=Level
                utt.save()
                response['Status']=True
            except Exception as e:
                response['error']="this uid is not join the team"
        else:
            response['error']="lost data"
        return JsonResponse(response)

def memberList(request):
    response={}
    response['members']=[]
    if request.method=="POST":
        TID = request.POST.get('TID')
        response['TID']=TID
        if TID:
            TID = int(TID)
            users = User_through_Team.objects.filter(Team_id=TID)
            for u in users:
                try:
                    user = User.objects.get(pk=u.User_id)
                    team = Team.objects.get(pk=TID)
                    member = {}
                    member['UID']=user.pk
                    member['Username']=user.User_name
                    member['Level']=u.level

                    if team.creater==user:
                        member['Founder']=True
                    else:
                        member['Founder']=False

                    if user.avatar:
                        member["AvatarUrl"]=user.avatar.path
                    else:
                        member["AvatarUrl"] = ""

                    response['members'].append(member)
                except Exception as e:
                    response['error']="database wrong"
                    print(e)
        else:
            response['error']="TID is illegal"
        return JsonResponse(response)

def kickMember(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        TID = request.POST.get('TID')
        UID = request.POST.get('UID')
        if TID and UID:
            TID = int(TID)
            UID = int(UID)
            try:
                team = Team.objects.get(pk=TID)
            except Exception as e:
                print(e)
                response['error']="TID wrong"
                return JsonResponse(response)
            try:
                utt = User_through_Team.objects.get(Team_id=TID,User_id=UID)
            except Exception as e:
                print(e)
                response['error']="this user didn't in this team"
                return JsonResponse(response)
            utt.delete()
            response['Status']=True
            return JsonResponse(response)
        else:
            response['error']="lost data"

def inviteMember(request):
    response={}
    response['Status']=False
    response['Exist']=True
    if request.method=="POST":
        TID = request.POST.get('TID')
        TargetEmail = request.POST.get('TargetEmail')
        if TID and TargetEmail:
            TID = int(TID)
            try:
                user = User.objects.get(User_email=TargetEmail)
            except Exception as e:
                print(e)
                response['Exist']=False
                response['error']="this user isn't exist"
                return JsonResponse(response)
            utt = User_through_Team.objects.filter(User=user,Team_id=TID)
            if utt:
                pass
            else:
                Inviter_through_Team.objects.create(User=user, Team_id=TID)
                response['Status'] = True
                response['Exist'] = False
        else:
            response['error']="lost data"
        return JsonResponse(response)

def dismissTeam(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        TID = request.POST.get('TID')
        if TID:
            TID = int(TID)
            try:
                team = Team.objects.get(pk=TID)
            except Exception as e:
                print(e)
                response['error']="TID wrong"
                return JsonResponse(response)
            team.delete()
            response['Status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def deleteFile(request):
    response={}
    response['status']=False
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        if UID and AID:
            try:
                UID = int(UID)
                AID = int(AID)
            except Exception as e:
                print(e)
                response['error']="AID or UID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                print(e)
                response['error']="this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                print(e)
                response['error']="this user isn't exist"
                return JsonResponse(response)
            if TID:
                try:
                    TID = int(TID)
                except Exception as e:
                    print(e)
                    response['error'] = "TID isn't a number"
                    return JsonResponse(response)
                try:
                    team = Team.objects.get(pk=TID)
                except Exception as e:
                    print(e)
                    response['error'] = "TID wrong"
                    return JsonResponse(response)
                try:
                    user_level = User_through_Team.objects.get(User_id=UID,Team_id=TID).level
                except Exception as e:
                    print(e)
                    response['error']="this user don't in this team"
                    return JsonResponse(response)
                if user_level >= document.Dnum:
                    document.delete()
                    response['status']=True
                else:
                    response['error']="low level"
            else:
                if document.User_id==UID:
                    document.delete()
                    response['status']=True
                elif document.deleteable:
                    document.delete()
                    response['status'] = True
                else:
                    response['error']="this document isn't this user's"
        else:
            response['error']="lost data"
        return JsonResponse(response)

def collectFile(request):
    response={}
    response['status']=False
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        if AID and UID:
            try:
                AID = int(AID)
                UID = int(UID)
                try:
                    dtc = Document_through_CollectUser.objects.get(User_id=UID,Document_id=AID)
                    response['error']="this user already collected this document"
                except Exception as e:
                    Document_through_CollectUser.objects.create(User_id=UID,Document_id=AID)
                    response['status']=True
            except Exception as e:
                print(e)
                response['error']="AID or UID isn't a number"
        else:
            response['error']="lost data"
        return JsonResponse(response)

def getUserAuthority(request):
    response={}
    response['CanRead']=False
    response['CanComment'] = False
    response['CanEdit'] = False
    response['UserLevel'] = 0
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        if UID and AID and TID:
            try:
                UID = int(UID)
                AID = int(AID)
                TID = int(TID)
            except Exception as e:
                print(e)
                response['error']="UID or AID or TID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                print(e)
                response['error'] = "this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                print(e)
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            try:
                team = Team.objects.get(pk=TID)
            except Exception as e:
                print(e)
                response['error'] = "this team isn't exist"
                return JsonResponse(response)
            try:
                user_level = User_through_Team.objects.get(User_id=UID, Team_id=TID).level
            except Exception as e:
                print(e)
                response['error'] = "this user don't in this team"
                return JsonResponse(response)

            if user_level >= document.Rnum:
                response['CanRead'] = True
            if user_level >= document.Enum:
                response['CanEdit'] = True
            if user_level >= document.Cnum:
                response['CanComment'] = True
            response['UserLevel'] = user_level
            return JsonResponse(response)
