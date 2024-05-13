from django.db import models

# Create your models here.
class user(models.Model):
    openid = models.CharField(max_length=32,unique=False)
    password = models.CharField(max_length=64)
    user_type = models.CharField(verbose_name="recruiter/tutor/TBD",max_length=16,blank=True)
    name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(verbose_name="male/female/TBD",max_length=8,blank=True)
    college = models.CharField(verbose_name="用户所在院校,可空",max_length=64, blank=True)
    self_intro = models.TextField(blank=True)
    session_key = models.CharField(max_length=64)
    nickName = models.CharField(max_length=64, blank=True)
    avatarUrl = models.URLField( blank=True)

class public_msg(models.Model):
    userid = models.ForeignKey("user",on_delete=models.CASCADE)
    msg_type = models.CharField(verbose_name="recruitment家长招聘/landjob老师求聘/TBD",max_length=16,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbs_up = models.IntegerField
    content = models.TextField(null=True, blank=True)

class chat_msg(models.Model):
    sender_id = models.ForeignKey("user",related_name='FriendList_sender_id',on_delete=models.CASCADE)
    receiver_id = models.ForeignKey("user",related_name='FriendList_receiver_id',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)   
    content = models.TextField(null=True, blank=True)