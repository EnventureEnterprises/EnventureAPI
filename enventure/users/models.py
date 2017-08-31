from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _
from bookkeeping.models import Cbo,Enventure


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    karma = models.IntegerField(default=1)
    phoneNumber = models.CharField(max_length=200,null=True,blank=True)
    cboName = models.CharField( max_length=200, blank=True,null=True)
    district = models.CharField( max_length=200, blank=True,null=True)
    post_views = models.IntegerField(default=0,blank=True,null=True)
    district = models.CharField( max_length=200, blank=True,null=True)
    is_registered  = models.NullBooleanField()
    first_login  = models.NullBooleanField()
    account_type = models.CharField( max_length=200, blank=True,null=True)
    address = models.CharField( max_length=200, blank=True,null=True)
    cbo = models.ForeignKey(Cbo,related_name="users",null=True)
    enventure = models.ForeignKey(Enventure,related_name="users",null=True)
    def __str__(self):
        return self.username

    def get_avatar():
    	return ""

    @property
    def name(self):
      return "%s %s"%(self.first_name,self.last_name)

    	
