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
    send_time = models.DateTimeField(auto_now_add=True,verbose_name="发送时间")
    content = models.CharField(max_length=64,verbose_name="文本内容",default=None)

    User = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="所有者",default=None)

class Team(models.Model):
    content = models.CharField(max_length=256,verbose_name="团队描述",default=None)
    team_name =  models.CharField(max_length=64,verbose_name="团队名")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    memebers = models.ManyToManyField('User',through = 'User_through_Team')

class Document(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    last_time = models.DateTimeField(auto_now=True,verbose_name="最后一次修改时间")
    content = models.TextField(verbose_name="文档内容")
    title = models.CharField(max_length=32,verbose_name="文档标题")

    file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name="所属文件夹", default=None,null=True)
    AuthorityUsers = models.ManyToManyField('User', through='Permission', related_name="Document_AuthorityUsers")
    EditUsers = models.ManyToManyField('User',through='Document_through_EditUser',related_name="Document_EditUsers")
    BrowseUsers = models.ManyToManyField('User',through='Document_through_BrowseUser',related_name="BrowseUsers")
    CollectUsers = models.ManyToManyField('User',through='Document_through_CollectUser',related_name="CollectUsers")
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="创建者", default=None, blank=False)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", default=None)

class File(models.Model):
    File_name = models.CharField(max_length=32,verbose_name="文件夹名字",default=None)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_time = models.DateTimeField(auto_now=True, verbose_name="最后一次修改时间")

    EditUsers = models.ManyToManyField('User', through='File_through_EditUser',related_name="File_EditUsers")
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="创建者",related_name="create_user" ,default=None, blank=False)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", default=None)

class Comment(models.Model):
    content = models.CharField(max_length=256,verbose_name="评价内容",default=None)

    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="评论者", default=None, blank=False)
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被评论文档", default=None, blank=False)

class Del_Document(models.Model):
    pass

#中间表部分
class User_through_Team(models.Model):
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="团队成员", default=None)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", default=None)
    join_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")

class Document_through_EditUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被修改文档", default=None, blank=False)
    User = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name="修改者",default=None,blank=False)
    Edit_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

class File_through_EditUser(models.Model):
    File = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name="被修改文件夹", default=None,
                                    blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="修改者", default=None, blank=False)
    Edit_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")


class Document_through_BrowseUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被浏览文档", default=None, blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="浏览者", default=None, blank=False)
    Edit_time = models.DateTimeField(auto_now_add=True, verbose_name="浏览时间")

class Document_through_CollectUser(models.Model):
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="被收藏文档", default=None, blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="收藏者", default=None, blank=False)
    Collect_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

class Permission(models.Model):
    Team =  models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name="团队", default=None, blank=False)
    Document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name="文档", default=None, blank=False)
    User = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="用户", default=None, blank=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    one = models.BooleanField(default=False)
    two = models.BooleanField(default=False)
    three = models.BooleanField(default=False)
    four = models.BooleanField(default=False)
    five = models.BooleanField(default=False)