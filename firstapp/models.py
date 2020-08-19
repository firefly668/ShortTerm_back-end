# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


# 实体部分
class User(models.Model):
    User_name = models.CharField(max_length=64,verbose_name="用户名",unique=True)
    User_email = models.EmailField(default=None,verbose_name="邮箱")
    avatar = models.ImageField(upload_to='', blank = True,default=None,verbose_name="头像")
    add_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    password = models.CharField(max_length=256,verbose_name="密码")

class Message(models.Model):
    TYPES = (
        ('Invitation','邀请'),
        ('Normal','普通')
    )
    send_time = models.DateTimeField(auto_now_add=True,verbose_name="发送时间")
    content = models.CharField(max_length=64,verbose_name="文本内容",default=None)
    read = models.BooleanField(default=False)
    type = models.CharField(max_length=64,verbose_name="消息类型",choices=TYPES,default='Normal')

    send_User = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="发送者",related_name="send_user",default=None,null=True)
    accept_User = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="接收者",related_name="accept_user",default=None)

class Team(models.Model):
    content = models.CharField(max_length=256,verbose_name="团队描述",default=None,null=True)
    team_name =  models.CharField(max_length=64,verbose_name="团队名")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    creater = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="创建者",default=None,related_name="creater")
    memebers = models.ManyToManyField('User',through = 'User_through_Team',related_name="menebers")

class Document(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    last_time = models.DateTimeField(auto_now=True,verbose_name="最后一次修改时间")
    content = models.TextField(verbose_name="文档内容")
    title = models.CharField(max_length=32,verbose_name="文档标题")

    MD5 = models.CharField(max_length=64,default="",verbose_name="加密信息")

    #置顶评论
    topcomment = models.IntegerField(default=-1)

    #浏览量 编辑量 评论量
    browse_num = models.IntegerField(default=0)
    edit_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    #回收站
    recycle = models.BooleanField(default=False)

    #模板
    model = models.BooleanField(default=False)

    #分享权限
    judgeable = models.BooleanField(default=False)
    readable = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)
    deleteable = models.BooleanField(default=False)

    #团队权限
    Rnum = models.IntegerField(default=1)
    Enum = models.IntegerField(default=1)
    Cnum = models.IntegerField(default=1)
    Dnum = models.IntegerField(default=1)

    EditUsers = models.ManyToManyField('User',through='Document_through_EditUser',related_name="EditUsers",verbose_name="修改用户记录")
    BrowseUsers = models.ManyToManyField('User',through='Document_through_BrowseUser',related_name="BrowseUsers",verbose_name="浏览用户记录")
    CollectUsers = models.ManyToManyField('User',through='Document_through_CollectUser',related_name="CollectUsers",verbose_name="收藏用户列表")
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="创建者", default=None, blank=False)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", default=None,null=True)

class Tag(models.Model):
    name = models.CharField(max_length=64,verbose_name="标签名")
    type = models.CharField(max_length=64,verbose_name="标签种类")

    Team = models.ForeignKey("Team",on_delete=models.CASCADE,verbose_name="",default=None,null=True)
    User = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="",default=None)
    document = models.ForeignKey("Document",on_delete=models.CASCADE,verbose_name="所属文档",default=None,null=True)

class Comment(models.Model):
    content = models.CharField(max_length=256,verbose_name="评价内容",default=None)
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name="评论时间")

    maincomment = models.ForeignKey('Comment',on_delete=models.CASCADE,verbose_name="回复评论",null=True,default=None)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="评论者", default=None,null=True)
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被评论文档", default=None,null=True)

class Image(models.Model):
    img = models.ImageField(upload_to='', blank = True,default=None,verbose_name="图片")

#中间表部分
class User_through_Team(models.Model):
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="团队成员", related_name="utt_User",default=None)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", related_name="utt_Team",default=None)
    level = models.IntegerField(verbose_name="团队等级",default=1)
    inviter = models.CharField(max_length=256,verbose_name="邀请者",default=None,null=True)
    join_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")

class Document_through_EditUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被修改文档", default=None, blank=False)
    User = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name="修改者",default=None,blank=False)
    Edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

class Document_through_BrowseUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被浏览文档", default=None, blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="浏览者", default=None, blank=False)
    Browse_time = models.DateTimeField(auto_now=True, verbose_name="浏览时间")

class Document_through_CollectUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被收藏文档", default=None, blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="收藏者", default=None, blank=False)
    Collect_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

class Inviter_through_Team(models.Model):
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="团队成员", related_name="itt_User",default=None)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", related_name="itt_Team",default=None)
    Message = models.ForeignKey("Message",on_delete=models.CASCADE,verbose_name="对应消息",related_name="itt_Message",default=None)
    inviter_time = models.DateTimeField(auto_now=True,verbose_name="邀请时间")
