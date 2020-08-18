from django.shortcuts import render
from django.db.models import Avg, Max, Min, Sum
from firstapp.models import User
from firstapp.models import Document
from firstapp.models import Team
from firstapp.models import Comment
from firstapp.models import Message
from firstapp.models import Image
from firstapp.models import Tag
from firstapp.models import Document_through_CollectUser
from firstapp.models import Document_through_BrowseUser
from firstapp.models import Document_through_EditUser
from firstapp.models import User_through_Team
from firstapp.models import Inviter_through_Team
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
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
                response['AvatarUrl'] = "media/img"+user[0].avatar.url
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
                #print(e)
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
                #print(e)
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
                #print(e)
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
                #print(e)
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
                #print(e)
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
                if user.avatar:
                    response['imageUrl']="/media/img"+user.avatar.url
                else:
                    response['imageUrl']=""
                return JsonResponse(response)
            except Exception as e:
                response['error']="user isn't exist."
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
    response['Status']=False
    if request.method=="POST":
        data = json.loads(request.body,strict=False)
        UID = data.get('UID',None)
        AID = data.get('AID',None)
        TID = data.get('TID',None)
        Content = data.get('Content',None)
        Title = data.get('Title',None)
        Tags = data.get('Tags',None)
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
                    Tag.objects.filter(document=document).delete()
                    for tag in Tags:
                        Tag.objects.create(name=tag['name'],type=tag['type'],document=document)
                    response['AID']=document.pk
                    Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    Document_through_BrowseUser.objects.create(Document=document,User_id=UID)
                    document.browse_num+=1
                    document.edit_num+=1
                    document.save()
                except Exception as e:
                    response['Status'] = False
                    return JsonResponse(response)
            else:
                try:
                    document = Document.objects.get(pk=AID)
                except Exception as e:
                    response['error'] = "AID wrong"
                    return JsonResponse(response)
                lastbrowse_time = Document_through_BrowseUser.objects.get(User_id=UID,document=document).Browse_time
                lastbrowse_time_str = datetime.datetime.strptime(lastbrowse_time,"%Y-%m-%d")
                lastedit_time_str = datetime.datetime.strptime(document.last_time,"%Y-%m-%d")
                if lastbrowse_time_str<lastedit_time_str:
                    return JsonResponse(response)
                document.title = Title
                document.content = Content
                if TID:
                    document.Team_id = int(TID)
                document.edit_num+=1
                document.save()
                Tag.objects.filter(document=document).delete()
                for tag in Tags:
                    Tag.objects.create(name=tag['name'], type=tag['type'], document=document)
                try:
                    dte = Document_through_EditUser.objects.get(Document=document,User_id=UID)
                    dte.Edit_time = datetime.datetime.now()
                except Exception as e:
                    Document_through_EditUser.objects.create(Document=document, User_id=UID)
                    response['warning']="last edition didn't record,but this time is done."
            response['Status'] = True
            return JsonResponse(response)
        else:
            response['error']="lost data"
            return JsonResponse(response)

def sendMyModel(request):
    response = {}
    response['Status'] = False
    if request.method == "POST":
        data = json.loads(request.body,strict=False)
        UID = data.get('UID', None)
        AID = data.get('AID', None)
        TID = data.get('TID', None)
        Content = data.get('Content', None)
        Title = data.get('Title', None)
        Tags = data.get('Tags', None)
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
                    for tag in Tags:
                        Tag.objects.create(name=tag['name'], type=tag['type'], document=document)
                    response['AID']=document.pk
                except Exception as e:
                    response['error'] = "UID wrong"
                    return JsonResponse(response)
            else:
                response['error']="AID!=-1"
                return JsonResponse(request)
            response['Status'] = True
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def getArticle(request):
    response={}
    response['Status'] = False
    response['Content'] = ""
    response['Title'] = ""
    response['Tags'] = []
    if request.method=="POST":
        AID = request.POST.get('AID')
        UID = request.POST.get('UID')
        if AID and UID:
            AID = int(AID)
            UID = int(UID)
            try:
                document = Document.objects.get(pk=AID)
                if document.recycle:
                    response['error'] = "you can't open a document which in recycle bin"
                    return JsonResponse(response)
                if document.model:
                    pass
                else:
                    try:
                        dtb = Document_through_BrowseUser.objects.get(Document=document,User_id=UID)
                        dtb.Browse_time = datetime.datetime.now()
                        dtb.save()
                    except Exception as e:
                        response['warning']="last browse didn't record,but this time is done."
                        dtb = Document_through_BrowseUser()
                        dtb.Document=document
                        dtb.User_id=UID
                        dtb.save()
                    document.browse_num += 1
                    document.save()
                response['Status'] = True
                response['Content'] = document.content
                response['Title'] = document.title
                tags = Tag.objects.filter(document=document)
                for tag in tags:
                    t={}
                    t['name']=tag.name
                    t['type']=tag.type
                    response['Tags'].append(t)
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
                        response['error']="team database wrong"

            documents1_B = Document_through_BrowseUser.objects.filter(User_id=UID,Browse_time__gte=(datetime.datetime.now() - datetime.timedelta(3)))
            if documents1_B:
                for documents1 in documents1_B:
                    try:
                        d = {}
                        document = Document.objects.get(pk=documents1.Document_id,recycle=False,model=False)
                        try:
                            dtc = Document_through_CollectUser.objects.get(Document=document,User_id=UID)
                            d['isCollect'] = True
                        except Exception as e:
                            d['isCollect'] = False
                        d['Tags']=[]
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)

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
                        pass

            documents2 = Document_through_EditUser.objects.filter(User_id=UID,Edit_time__gte=(datetime.datetime.now() - datetime.timedelta(3)))
            if documents2:
                for document in documents2:
                    try:
                        d = {}
                        dt = Document.objects.get(pk=document.Document_id,recycle=False)
                        try:
                            dtc = Document_through_CollectUser.objects.get(Document=dt,User_id=UID)
                            d['isCollect'] = True
                        except Exception as e:
                            d['isCollect'] = False
                        d['Tags'] = []
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)
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
                        pass

            documents3 = Document_through_CollectUser.objects.filter(User_id=UID)
            if documents3:
                for document in documents3:
                    try:
                        d={}
                        dt = Document.objects.get(pk=document.Document_id,recycle=False)
                        d['Tags'] = []
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)
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
                        pass

            documents4 = Document.objects.filter(User_id=UID,model=True,recycle=False)
            if documents4:
                for document in documents4:
                    if document.Team:
                        continue
                    else:
                        d={}
                        d['Tags'] = []
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)
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
                    t['teamName']=tm.team_name
                    response['teams'].append(t)
                except Exception as e:
                    #print(e)
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
    response['TID'] = -1
    if request.method=="POST":
        TID = request.POST.get('TID')
        if TID:
            try:
                TID = int(TID)
            except Exception as e:
                response['error']="TID isn't a number"
                return JsonResponse(response)
            response['TID'] = TID
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
                        member["AvatarUrl"]="/media/img"+user.avatar.url
                    else:
                        member["AvatarUrl"] = ""

                    response['members'].append(member)
                except Exception as e:
                    response['error']="database wrong"
                    #print(e)
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
                user = User.objects.get(pk=UID)
                team = Team.objects.get(pk=TID)
            except Exception as e:
                #print(e)
                response['error']="TID or UID wrong"
                return JsonResponse(response)
            try:
                utt = User_through_Team.objects.get(Team_id=TID,User_id=UID)
            except Exception as e:
                #print(e)
                response['error']="this user didn't in this team"
                return JsonResponse(response)

            utt.delete()
            utts = User_through_Team.objects.filter(Team_id=TID)
            content = user.User_name + "已被踢出了" + team.team_name
            for mutt in utts:
                Message.objects.create(content=content, type="Normal", accept_User_id=mutt.User_id)
            content = "您已被踢出团队：" + team.team_name
            Message.objects.create(content=content,accept_User_id=UID)
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
                #print(e)
                response['Exist']=False
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                team = Team.objects.get(pk=TID)
            except Exception as e:
                response['error']="this team isn't exist"
                return JsonResponse(response)
            utt = User_through_Team.objects.filter(User=user,Team_id=TID)
            if utt:
                response['error']="this user already in this team"
            else:
                content=team.team_name
                content+="邀请你加入他们"
                me = Message.objects.create(content=content,type="Invitation",accept_User=user)
                Inviter_through_Team.objects.create(User=user, Team_id=TID,Message=me)
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
                #print(e)
                response['error']="TID wrong"
                return JsonResponse(response)
            utts = User_through_Team.objects.filter(Team_id=TID)
            content = "您的团队：" + team.team_name +"已解散"
            for utt in utts:
                Message.objects.create(content=content,accept_User=utt.User)
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
                #print(e)
                response['error']="AID or UID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                #print(e)
                response['error']="this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                #print(e)
                response['error']="this user isn't exist"
                return JsonResponse(response)
            if TID:
                try:
                    TID = int(TID)
                except Exception as e:
                    #print(e)
                    response['error'] = "TID isn't a number"
                    return JsonResponse(response)
                try:
                    team = Team.objects.get(pk=TID)
                except Exception as e:
                    #print(e)
                    response['error'] = "TID wrong"
                    return JsonResponse(response)
                try:
                    user_level = User_through_Team.objects.get(User_id=UID,Team_id=TID).level
                except Exception as e:
                    #print(e)
                    response['error']="this user don't in this team"
                    return JsonResponse(response)
                if user_level >= document.Dnum:
                    document.recycle=True
                    document.save()
                    response['status']=True
                else:
                    response['error']="low level"
            else:
                if document.User_id==UID:
                    document.recycle=True
                    document.save()
                    response['status']=True
                elif document.deleteable:
                    document.recycle=True
                    document.save()
                    response['status'] = True
                else:
                    response['error']="this document isn't this user's or low level"
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
            except Exception as e:
                #print(e)
                response['error']="AID or UID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID,recycle=False)
            except Exception as e:
                response['error']="this document isn't exist or in recyclebin"
                return JsonResponse(response)
            try:
                dtc = Document_through_CollectUser.objects.get(User_id=UID, Document_id=AID)
                response['error'] = "this user already collected this document"
            except Exception as e:
                Document_through_CollectUser.objects.create(User_id=UID, Document_id=AID)
                response['status'] = True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def unCollectFile(request):
    response={}
    response['status']=False
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        if UID and AID:
            try:
                UID = int(UID)
                AID = int(AID)
            except Exception as e:
                response['error']="UID or AID isn't a number"
                return JsonResponse(response)
            try:
                dtc = Document_through_CollectUser.objects.get(User_id=UID,Document_id=AID)
            except Exception as e:
                response['error']="this user han't collect this document yet."
                return JsonResponse(response)
            dtc.delete()
            response['status']=True
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
                #print(e)
                response['error']="UID or AID or TID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                #print(e)
                response['error'] = "this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                #print(e)
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            try:
                team = Team.objects.get(pk=TID)
            except Exception as e:
                #print(e)
                response['error'] = "this team isn't exist"
                return JsonResponse(response)
            try:
                user_level = User_through_Team.objects.get(User_id=UID, Team_id=TID).level
            except Exception as e:
                #print(e)
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

def CommentList(request):
    response={}
    response['comments']=[]
    response['feedback']=False
    if request.method=="POST":
        AID = request.POST.get('AID')
        if AID:
            try:
                AID = int(AID)
            except Exception as e:
                response['error']="AID isn't a number"
                return JsonResponse
            comments = Comment.objects.filter(Document_id=AID)
            for comment in comments:
                if comment.maincomment:
                    continue
                else:
                    ct = {}
                    try:
                        user = User.objects.get(pk=comment.User_id)
                    except Exception as e:
                        response['error']="database wrong"
                        return JsonResponse(response)
                    ct['cid'] = comment.pk
                    ct['content']=comment.content
                    ct['email']=user.User_email
                    ct['inputShow']=False
                    ct['name']=user.User_name
                    ct['time']=comment.comment_time
                    ct['uid']=user.pk
                    if user.avatar:
                        ct['imageurl']="media/img"+user.avatar.url
                    else:
                        ct['imageurl'] =""
                    ct['reply']=[]
                    replycomments = Comment.objects.filter(maincomment=comment.pk)
                    for replycomment in replycomments:
                        rt={}
                        try:
                            reply_user = User.objects.get(pk=replycomment.User_id)
                        except Exception as e:
                            response['error'] = "database wrong"
                            return JsonResponse(response)
                        rt['cid']=replycomment.pk
                        rt['content']=replycomment.content
                        rt['email']=reply_user.User_email
                        rt['inputShow']=False
                        rt['name']=reply_user.User_name
                        rt['time']=replycomment.comment_time
                        rt['to']=user.User_name
                        rt['uid']=reply_user.pk
                        if reply_user.avatar:
                            rt['imageurl']="media/img"+reply_user.avatar.url
                        else:
                            rt['imageurl'] =""
                        ct['reply'].append(rt)
                    response['comments'].append(ct)
            response['feedback']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def DeleteComment(request):
    response={}
    response['feedback']=False
    if request.method=="POST":
        CID = request.POST.get('CID')
        if CID:
            try:
                CID = int(CID)
            except Exception as e:
                response['error']="CID isn't a number"
                return JsonResponse(response)
            try:
                comment = Comment.objects.get(pk=CID)
            except Exception as e:
                response['error']="this comment isn't exist"
                return JsonResponse(response)
            document = comment.Document
            document.comment_num-=1
            document.save()
            comment.delete()
            response['feedback']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def NewComment(request):
    response={}
    response['CID']=-1
    if request.method=="POST":
        AID = request.POST.get('AID')
        UID = request.POST.get('UID')
        content = request.POST.get('content')
        if AID and UID and content:
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                response['error']="this document isn't exist"
                return JsonResponse(response)
            document.comment_num+=1
            document.save()
            comment = Comment()
            comment.Document=document
            comment.User=user
            comment.content=content
            comment.save()
            response['CID']=comment.pk
        else:
            response['error']="lost data"
        return JsonResponse(response)

def ReplyComment(request):
    response={}
    response['CID']=-1
    if request.method=="POST":
        data = json.loads(request.body,strict=False)
        RPID = data.get('RPID',None)
        replycomment = data.get('comment',None)
        if RPID and replycomment:
            try:
                comment = Comment.objects.get(pk=RPID)
            except Exception as e:
                response['error']="this comment isn't exist"
                return JsonResponse(response)
            try:
                replycomment['UID'] = int(replycomment['UID'])
                replycomment['AID'] = int(replycomment['AID'])
            except Exception as e:
                response['error']="AID or UID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=replycomment['UID'])
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=replycomment['AID'])
            except Exception as e:
                response['error']="this document isn't exist"
                return JsonResponse(response)
            document.comment_num+=1
            document.save()
            rt = Comment()
            rt.content=replycomment['content']
            rt.User = user
            rt.Document = document
            rt.maincomment_id = comment.pk
            rt.save()
            response['CID']=rt.pk
        else:
            response['error']="lost data"
        return JsonResponse(response)

def myMessage(request):
    response={}
    response['UnRead']=0
    response['messages']=[]
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            try:
                UID = int(UID)
            except Exception as e:
                response['error']="UID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            messages = Message.objects.filter(accept_User_id=UID)
            for message in messages:
                me = {}
                me['MessageID']=message.pk
                me['Content']=message.content
                me['Time']=message.send_time
                me['Type']=message.type
                me['Read']=message.read
                if not message.read:
                    response['UnRead']+=1
                response['messages'].append(me)
        else:
            response['error']="lost data"
        return JsonResponse(response)

def readMessage(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        data = json.loads(request.body,strict=False)
        messages = data.get('Messages',None)
        if messages:
            for mid in messages:
                MID = int(mid['MessageID'])
                try:
                    message = Message.objects.get(pk=MID)
                except Exception as e:
                    response['error']="one of message isn't exist"
                    return JsonResponse(response)
                message.read=True
                message.save()
            response['Status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def replyInvitation(request):
    response={}
    response['Status']=False
    response['Name']=""
    if request.method=="POST":
        MID = request.POST.get('MID')
        Opr = request.POST.get('Opr')
        if MID and Opr:
            try:
                message = Message.objects.get(pk=MID)
            except Exception as e:
                response['error']="this message isn't exist"
                return JsonResponse(response)
            try:
                itt = Inviter_through_Team.objects.get(Message_id=MID)
                team = Team.objects.get(pk=itt.Team_id)
            except Exception as e:
                response['error']="database wrong"
                return JsonResponse(response)
            if Opr:
                utt = User_through_Team()
                utt.User_id=itt.User_id
                utt.Team=team
                if message.send_User:
                    utt.inviter=message.send_User
                utt.save()
            message.delete()
            response['Status']=True
            response['Name']=team.team_name
        else:
            response['error']="lost data"
        return  JsonResponse(response)

def TeamInfo(request):
    response={}
    response['team']={}
    response['mylevel']=0
    response['Documents1']=[]
    response['Documents4']=[]
    if request.method=="POST":
        UID = request.POST.get('UID')
        TID = request.POST.get('TID')
        if UID and TID:
            try:
                UID = int(UID)
                TID = int(TID)
            except Exception as e:
                response['error']="UID or TID isn't number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                team = Team.objects.get(pk=TID)
                response['team']['TID']=team.pk
                response['team']['name']=team.team_name
                response['team']['describe']=team.content
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                utt = User_through_Team.objects.get(User_id=UID,Team_id=TID)
                response['mylevel']=utt.level
            except Exception as e:
                response['error']="database_utt wrong"
                return JsonResponse(response)

            documents1 = Document.objects.filter(Team_id=TID,model=False,recycle=False)
            for document1 in documents1:
                dt={}
                try:
                    dtc = Document_through_CollectUser.objects.get(Document=document1,User_id=UID)
                    dt['isCollect'] = True
                except Exception as e:
                    dt['isCollect'] = False
                dt['lastEditDate']=document1.last_time
                dt['documentName']=document1.title
                dt['documentOwner']=document1.User.User_name
                dt['AID']=document1.pk
                dt['UID']=document1.User_id
                dt['TID']=document1.Team_id
                response['Documents1'].append(dt)

            documents4 = Document.objects.filter(Team_id=TID,model=True,recycle=False)
            for document4 in documents4:
                dt={}
                dt['documentName']=document4.title
                dt['TID']=document4.Team_id
                dt['MID']=document4.pk
                response['Documents4'].append(dt)
        else:
            response['error']="lost data"
        return JsonResponse(response)

def avatarUrl(request):
    response={}
    response['status']=False
    if request.method=="POST":
        file = request.FILES.get('file')
        UID = request.POST.get('UID')
        if UID :
            try:
                UID = int(UID)
            except Exception as e:
                response['error']="UID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist."
                return JsonResponse(response)
            file_name = str(UID)+".jpg"
            save_path = settings.MEDIA_ROOT  + file_name
            with open(save_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)
            user.avatar=file_name
            user.save()
            response['avatarUrl']="/media/img/" + file_name
            response['status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def picSave(request):
    response={}
    response['imgUrl']=""
    if request.method=="POST":
        img = request.FILES.get('img')
        imgs = Image.objects.all()
        if imgs:
            number = imgs.aggregate(Max('pk'))['pk__max'] + 1
        else:
            number = 1
        file_name ="d"+ str(number)+".jpg"
        save_path = settings.MEDIA_ROOT + file_name
        with open(save_path,'wb') as f:
            for content in img.chunks():
                f.write(content)
        Image.objects.create(img=file_name)
        response['imgUrl']="/media/img/"+file_name
        return JsonResponse(response)

def authJudger(request):
    response={}
    response['Status']=False
    response['PrivateOwn']=False
    response['TeamOwn']=False
    response['CanRead']=False
    response['CanComment']=False
    response['CanEdit']=False
    if request.method=="POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        if UID and AID:
            try:
                UID = int(UID)
                AID = int(AID)
            except Exception as e:
                response['error']="UID or AID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                response['error']="this document isn't exist"
                return JsonResponse(response)
            if document.Team:
                try:
                    utt = User_through_Team.objects.get(User_id=UID,Team=document.Team)
                    response['TeamOwn']=True
                    response['Status']=True
                    return JsonResponse(response)
                except Exception as e:
                    pass
            if document.User==user:
                response['PrivateOwn']=True
            else:
                response['CanRead']=document.readable
                response['CanComment']=document.judgeable
                response['CanEdit']=document.editable
            response['Status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def completeDeleteFile(request):
    response = {}
    response['status'] = False
    if request.method == "POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        if UID and AID:
            try:
                UID = int(UID)
                AID = int(AID)
            except Exception as e:
                # print(e)
                response['error'] = "AID or UID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                # print(e)
                response['error'] = "this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                # print(e)
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            if TID:
                try:
                    TID = int(TID)
                except Exception as e:
                    # print(e)
                    response['error'] = "TID isn't a number"
                    return JsonResponse(response)
                try:
                    team = Team.objects.get(pk=TID)
                except Exception as e:
                    # print(e)
                    response['error'] = "TID wrong"
                    return JsonResponse(response)
                try:
                    user_level = User_through_Team.objects.get(User_id=UID, Team_id=TID).level
                except Exception as e:
                    # print(e)
                    response['error'] = "this user don't in this team"
                    return JsonResponse(response)
                if user_level >= document.Dnum:
                    document.delete()
                    response['status'] = True
                else:
                    response['error'] = "low level"
            else:
                if document.User_id == UID:
                    document.delete()
                    response['status'] = True
                elif document.deleteable:
                    document.delete()
                    response['status'] = True
                else:
                    response['error'] = "this document isn't this user's or low level"
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def restoreFile(request):
    response = {}
    response['status'] = False
    if request.method == "POST":
        UID = request.POST.get('UID')
        AID = request.POST.get('AID')
        TID = request.POST.get('TID')
        if UID and AID:
            try:
                UID = int(UID)
                AID = int(AID)
            except Exception as e:
                # print(e)
                response['error'] = "AID or UID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                # print(e)
                response['error'] = "this document isn't exist"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                # print(e)
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            if TID:
                try:
                    TID = int(TID)
                except Exception as e:
                    # print(e)
                    response['error'] = "TID isn't a number"
                    return JsonResponse(response)
                try:
                    team = Team.objects.get(pk=TID)
                except Exception as e:
                    # print(e)
                    response['error'] = "TID wrong"
                    return JsonResponse(response)
                try:
                    user_level = User_through_Team.objects.get(User_id=UID, Team_id=TID).level
                except Exception as e:
                    # print(e)
                    response['error'] = "this user don't in this team"
                    return JsonResponse(response)
                if user_level >= document.Dnum:
                    document.recycle = False
                    document.save()
                    response['status'] = True
                else:
                    response['error'] = "low level"
            else:
                if document.User_id == UID:
                    document.recycle = False
                    document.save()
                    response['status'] = True
                elif document.deleteable:
                    document.recycle = False
                    document.save()
                    response['status'] = True
                else:
                    response['error'] = "this document isn't this user's or low level"
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def quitTeam(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        UID = request.POST.get('UID')
        TID = request.POST.get('TID')
        if UID and TID:
            try:
                UID = int(UID)
                TID = int(TID)
            except Exception as e:
                response['error']="UID or TID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
                team = Team.objects.get(pk=TID)
                utt = User_through_Team.objects.get(User_id=UID,Team_id=TID)
            except Exception as e:
                response['error']="user or team isn't exist or user isn't in team"
                return JsonResponse(response)
            utt.delete()
            utts = User_through_Team.objects.filter(Team_id=TID)
            content = user.User_name + "已主动退出了" + team.team_name
            for mutt in utts:
                Message.objects.create(content=content,type="Normal",accept_User_id=mutt.User_id)
            response['Status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def someInfo1(request):
    response = {}
    response['myTeam'] = []
    response['Documents1'] = []
    response['Documents2'] = []
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            UID = int(UID)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)

            teams = User_through_Team.objects.filter(User_id=UID)
            for team in teams:
                try:
                    t = {}
                    tm = Team.objects.get(pk=team.Team_id)
                    t['TID']=tm.pk
                    t['teamName']=tm.team_name
                    response['myTeam'].append(t)
                except Exception as e:
                    response['error']="team database wrong"

            documents = Document.objects.filter(User_id=UID,recycle=False)
            for document in documents:
                if document.Team:
                    continue
                else:
                    if document.model:
                        d = {}
                        d['Tags'] = []
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)
                        d['documentName'] = document.title
                        d['UID'] = document.User_id
                        d['MID'] = document.pk
                        response['Documents2'].append(d)
                    else:
                        d = {}
                        try:
                            dtc = Document_through_CollectUser.objects.get(Document=document,User_id=UID)
                            d['isCollect'] = True
                        except Exception as e:
                            d['isCollect'] = False
                        d['Tags'] = []
                        tags = Tag.objects.filter(document=document)
                        for tag in tags:
                            t = {}
                            t['name'] = tag.name
                            t['type'] = tag.type
                            d['Tags'].append(t)
                        d['documentName'] = document.title
                        d['lastEditDate'] = document.last_time
                        d['AID'] = document.pk
                        d['TID'] = ""
                        d['documentOwner']=user.User_name
                        response['Documents1'].append(d)
            return JsonResponse(response)

def someInfo2(request):
    response = {}
    response['myTeam'] = []
    response['Documents1'] = []
    if request.method=="POST":
        UID = request.POST.get('UID')
        if UID:
            UID = int(UID)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)

            teams = User_through_Team.objects.filter(User_id=UID)
            for team in teams:
                try:
                    t = {}
                    tm = Team.objects.get(pk=team.Team_id)
                    t['TID'] = tm.pk
                    t['teamName'] = tm.team_name
                    response['myTeam'].append(t)
                except Exception as e:
                    response['error'] = "team database wrong"

            documents = Document.objects.filter(User_id = UID,recycle=True)
            for document in documents:
                if document.Team:
                    continue
                else:
                    d = {}
                    d['Tags'] = []
                    tags = Tag.objects.filter(document=document)
                    for tag in tags:
                        t = {}
                        t['name'] = tag.name
                        t['type'] = tag.type
                        d['Tags'].append(t)
                    d['documentName'] = document.title
                    d['lastEditDate'] = document.last_time
                    d['AID'] = document.pk
                    d['TID'] = ""
                    d['documentOwner'] = user.User_name
                    response['Documents1'].append(d)
            return JsonResponse(response)

def changeTeamDescription(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        TID = request.POST.get('TID')
        UID = request.POST.get('UID')
        Words = request.POST.get('Words')
        if TID and UID:
            try:
                UID = int(UID)
                TID = int(TID)
            except Exception as e:
                response['error'] = "UID or TID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
                team = Team.objects.get(pk=TID)
                utt = User_through_Team.objects.get(User_id=UID, Team_id=TID)
            except Exception as e:
                response['error'] = "user or team isn't exist or user isn't in team"
                return JsonResponse(response)
            team.content=Words
            team.save()
            utts = User_through_Team.objects.filter(Team_id=TID)
            content = user.User_name + "将" + team.team_name + "的团队描述修改为" + Words
            for mutt in utts:
                Message.objects.create(content=content, type="Normal", accept_User_id=mutt.User_id)
            response['Status'] = True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def TeamInfo2(request):
    response = {}
    response['team'] = {}
    response['mylevel'] = 0
    response['Documents1'] = []
    response['Documents4'] = []
    if request.method == "POST":
        UID = request.POST.get('UID')
        TID = request.POST.get('TID')
        if UID and TID:
            try:
                UID = int(UID)
                TID = int(TID)
            except Exception as e:
                response['error'] = "UID or TID isn't number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            try:
                team = Team.objects.get(pk=TID)
                response['team']['TID'] = team.pk
                response['team']['name'] = team.team_name
                response['team']['describe'] = team.content
            except Exception as e:
                response['error'] = "this user isn't exist"
                return JsonResponse(response)
            try:
                utt = User_through_Team.objects.get(User_id=UID, Team_id=TID)
                response['mylevel'] = utt.level
            except Exception as e:
                response['error'] = "database_utt wrong"
                return JsonResponse(response)
            documents1 = Document.objects.filter(Team_id=TID,recycle=True)
            for document1 in documents1:
                dt = {}
                dt['lastEditDate'] = document1.last_time
                dt['documentName'] = document1.title
                dt['documentOwner'] = document1.User.User_name
                dt['AID'] = document1.pk
                dt['UID'] = document1.User_id
                dt['TID'] = document1.Team_id
                response['Documents1'].append(dt)

            documents4 = Document.objects.filter(Team_id=TID, model=True)
            for document4 in documents4:
                dt = {}
                dt['documentName'] = document4.title
                dt['TID'] = document4.Team_id
                dt['MID'] = document4.pk
                response['Documents4'].append(dt)
        else:
            response['error'] = "lost data"
        return JsonResponse(response)

def deleteMessage(request):
    response={}
    response['Status']=False
    if request.method=="POST":
        data = json.loads(request.body,strict=False)
        UID = data.get('UID',None)
        MID = data.get('MID',None)
        if UID and MID:
            try:
                UID = int(UID)
            except Exception as e:
                response['error']="UID isn't a number"
                return JsonResponse(response)
            try:
                user = User.objects.get(pk=UID)
            except Exception as e:
                response['error']="this user isn't exist"
                return JsonResponse(response)
            for mid in MID:
                try:
                    message = Message.objects.get(accept_User_id=UID,pk=mid)
                except Exception as e:
                    response['error']="this message isn't exist or it's not belong this user"
                    return JsonResponse(response)
                message.delete()
            response['Status']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def AIDgetTID(request):
    response={}
    response['feedback']=False
    response['TID']=""
    if request.method=="POST":
        AID = request.POST.get('AID')
        if AID :
            try:
                AID = int(AID)
            except Exception as e:
                response['error']="AID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                response['error']="this document isn't exist"
                return JsonResponse(response)
            response['TID']=document.Team_id
            response['feedback']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)

def getcheckNum(request):
    response={}
    response['checknum']=0
    response['editnum']=0
    response['commentnum']=0
    response['feedback']=False
    if request.method=="POST":
        AID = request.POST.get('AID')
        if AID:
            try:
                AID = int(AID)
            except Exception as e:
                response['error']="AID isn't a number"
                return JsonResponse(response)
            try:
                document = Document.objects.get(pk=AID)
            except Exception as e:
                response['error']="this document isn't exist"
                return JsonResponse(response)
            response['checknum']=document.browse_num
            response['editnum']=document.edit_num
            response['commentnum']=document.comment_num
            response['feedback']=True
        else:
            response['error']="lost data"
        return JsonResponse(response)




