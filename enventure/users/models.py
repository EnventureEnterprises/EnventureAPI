from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.CharField(max_length=200,default="http://urb.sparkpl.ug/static/images/avatar.png")
    karma = models.IntegerField(default=1)
    mobile = models.CharField(max_length=200,null=True,blank=True)
    gender = models.CharField( max_length=6, blank=True,null=True)
    post_views = models.IntegerField(default=0,blank=True,null=True)
    post_shares = models.IntegerField(default=0,blank=True,null=True)
    notify_of_friend_activity = models.NullBooleanField()
    notify_of_comments = models.NullBooleanField()
    notify_of_likes = models.NullBooleanField()
    is_facebook = models.NullBooleanField()
    is_twitter = models.NullBooleanField()
    current_login  = models.CharField(max_length=200,null=True,blank=True)
    is_mobile  = models.NullBooleanField()
    posts_count = models.IntegerField(default=0,blank=True,null=True)
    likes_count = models.IntegerField(default=0,blank=True,null=True)
    unread_notifications_count = models.IntegerField(default=0,blank=True,null=True)
    send_newsletter = models.NullBooleanField()
    is_registered  = models.NullBooleanField()
    


    def __str__(self):
        return self.username

    def get_avatar():
    	return ""

    @property
    def name(self):
      return "%s %s"%(self.first_name,self.last_name)

    	
