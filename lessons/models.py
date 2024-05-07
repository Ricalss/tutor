from django.db import models

# Create your models here.
class user(models.Model):
    openid = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    user_type = models.CharField(verbose_name="recruiter/tutor/TBD",max_length=16,default="TBD")
    name = models.CharField(max_length=64,default="TBD")
    gender = models.CharField(verbose_name="male/female/TBD",max_length=8,default="TBD")
    college = models.CharField(verbose_name="用户所在院校,可空",max_length=64,null=True, blank=True)
    self_into = models.TextField(null=True, blank=True)
    avatar = models.ImageField


class public_msg(models.Model):
    userid = models.ForeignKey("user",on_delete=models.CASCADE)
    msg_type = models.CharField(verbose_name="recruitment/hunt_for_tutor/TBD",max_length=16,default="TBD")
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbs_up = models.IntegerField
    content = models.TextField

#class private_chatlist(models.Model):
    
class private_msg(models.Model):
    sender_id = models.ForeignKey("user",related_name='FriendList_sender_id',on_delete=models.CASCADE)
    receiver_id = models.ForeignKey("user",related_name='FriendList_receiver_id',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)   
    content = models.TextField
