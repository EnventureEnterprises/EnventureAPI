from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.db import  models as djmodels
import tagulous
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
from mptt.models import MPTTModel, TreeForeignKey

from versatileimagefield.fields import VersatileImageField
from django.core.urlresolvers import reverse
from django.conf import settings
from . import utils
from django.db.models.signals import post_save
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from versatileimagefield.registry import versatileimagefield_registry
from django.utils.six import BytesIO

from PIL import Image

from versatileimagefield.datastructures import SizedImage
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal



class Account(MPTTModel):
    name = models.CharField(max_length=50)

    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children'
    )
    quantity = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2,default=Decimal("0"))
    amount_remaining = models.DecimalField(max_digits=16, decimal_places=2,default=Decimal("0"))
    order = models.CharField(max_length=8, blank=True, editable=False,null=True)
    code = models.CharField(max_length=8, blank=True)
    customer_mobile = models.CharField(max_length=8, blank=True,null=True)
    total_price = models.DecimalField(max_digits=16, decimal_places=2,default=Decimal("0"))
    cbo = models.ForeignKey("Cbo", db_column='cbo', related_name='cbo_accounts',null=True)
    entries = models.ForeignKey("Entry",related_name="cbo_entries",null=True)
    type =  models.CharField(max_length=8, blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ('order',)


class AssetAccount(Account):
    pass

class LiabilityAccount(Account):
    pass

class IncomeAccount(Account):
    pass

class ExpenseAccount(Account):
    pass

class EquityAccount(Account):
    pass




class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    number = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey("Item",related_name="entry_items",null=True)
    cbo = models.ForeignKey("Cbo",null=True)
    credit = models.ForeignKey("Account",related_name="credits",null=True)
    debit = models.ForeignKey("Account",related_name="debits",null=True)
    quantity = models.IntegerField(blank=True, null=True)

    date = models.DateField(blank=True, null=True)
    opening = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    closing = models.DecimalField(max_digits=16, decimal_places=2,null=True)

    amount = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    type =  models.CharField(max_length=64, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    customer_mobile =  models.CharField(max_length=64, blank=True, null=True)
    total_price = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    amount_paying = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    amount_remaining = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    sale_value = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    name = models.CharField(max_length=8, blank=True,null=True)
    transaction_type = models.CharField(max_length=64, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def _item(self):
      return self.item.name


class Cbo(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children'
    )
    users = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="cbos",null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    location = LocationField(based_fields=['place'], zoom=7, default=Point(1.0, 1.0))
    place = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def accounts(self):
        #sorting?
        return self.account_objects.all()

    def get_account(self, name):
        return self.account_objects.get(name=name)

class Item(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2,null=True)
    image = VersatileImageField(upload_to='files/%Y/%m/%d',null=True,blank=True)
    enabled = models.BooleanField( default=True)
    sales = models.ForeignKey(Entry,related_name = "sales",null=True,blank=True)
    inventory = models.ForeignKey(Entry,related_name = "inventory_updates",null=True)
    installments = models.ForeignKey(Entry,related_name = "installment_payments",null=True)
    debtors = models.ForeignKey(Account,related_name = "debtors",null=True)
    debit_account = models.ForeignKey(Account,related_name="debit_items",null=True,blank=True)
    credit_account = models.ForeignKey(Account,related_name="credit_items",null=True,blank=True)
    description = models.CharField(max_length=64, blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def debit(self):
        return currency_display(-self.amount) if self.amount < 0 else ''

    def credit(self):
        return currency_display(self.amount) if self.amount > 0 else ''



class Installation(djmodels.Model):
    token = models.TextField( blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "%s"%(self.token)



class Device(djmodels.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField( default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    device_id = models.TextField( blank=True, null=True, db_index=True)
    registration_id = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "%s %s"%(self.name,self.device_id)


    def send_notification(self,body,title):
        data={
            "to" : self.device_id,
            "notification" : {
              "body" : body,
              "title" : title

           }}


        utils.send_to_firebase(data)
        return True

    def send_data(self,nick,body,room,action):
        data = {
            "to" : self.device_id,
            "data" : {
            "Nick" : nick,
            "body" : body,
            "Room" : room,
            "action":action
            }
        }
        utils.send_to_firebase(data)
        return True

    def send_data_notification(self,nick,title,body,room,icon,action):
        data = {
                "to" : self.device_id,
                "notification" : {
                  "body" : body,
                  "title" : title,
                  "icon" : icon
                },
                "data" : {
                    "action":action,
                  "Nick" : nick,
                  "Room" : room
                }
              }
        utils.send_to_firebase(data)
        return True




    def send_adv_notification(self,nick,title,body,room,icon,action,
                              expiry,url,dialog_title,dialog_text,dialog_yes,dialog_no,min_version,max_version):
         data = {
                "to" : self.device_id,
                "notification" : {
                  "body" : body,
                  "title" : title,
                  "icon" : icon
                },
                "data" : {
                    "action":action,
                  "Nick" : nick,
                  "Room" : room,
                    "expiry":expiry,
                    "url":url,
                    "dialog_title":dialog_title,
                    "dialog_text":dialog_text,
                    "dialog_yes":dialog_yes,
                    "dialog_no":dialog_no,
                    "min_version":min_version,
                   "max_version":max_version


                }
              }
         utils.send_to_firebase(data)
         return True





class Notification(djmodels.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications",blank=True,null=True)
    message = models.TextField()
    minVersion = models.CharField(max_length=255, blank=True, null=True)
    maxVersion = models.CharField(max_length=255, blank=True, null=True)
    expiry = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    dialogYes = models.CharField(max_length=255, blank=True, null=True)
    dialogNo = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "%s"%(self.message)

    def get_absolute_url(self):
        return reverse('bookkeeping:notification-detail', args=[str(self.id)])

def send_response(sender, instance, created, **kwargs):
    if not created:
        devices = Device.objects.filter(user=instance.user)
        for device in devices:
            device.send_notification(instance.response,"Feedback Response")

def send_notification(sender, instance, created, **kwargs):
    if created:
        devices = Device.objects.all()
        for device in devices:
            device.send_notification(instance.message,"Urb")


def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        devices = Device.objects.filter(user=instance.post.user)
        for device in devices:
             if instance.creator == device.user:
                 pass
             else:
                device.send_notification("@%s says %s"%(instance.user.username,instance.text),"New Comment")

def send_post_notification(sender, instance, created, **kwargs):
    if created:
        prefs = Pref.objects.all()
        for pref in prefs:
            if Pref.objects.filter(location__distance_lt=(pref.location, Distance(km=pref.search_radius))).exists():
                devs = Device.objects.filter(user=pref.user)
                for d in devs:
                    if instance.creator == d.user:
                        pass
                    else:
                        d.send_notification("New Post Created %s"%instance.title,"New Post")


def warm_image(sender, instance, **kwargs):
    image_warmer = VersatileImageFieldWarmer(instance_or_queryset=Post.objects.filter(pk=instance.pk),rendition_key_set='image_gallery',image_attr='image')
    num_created, failed_to_create = image_warmer.warm()



#post_save.connect(send_response, sender=Feedback,weak=False)
#post_save.connect(warm_image, sender=Post,weak=False)
#post_save.connect(send_notification, sender=Notification,weak=False)
#post_save.connect(send_post_notification, sender=Post,weak=False)
#post_save.connect(send_comment_notification, sender=Comment,weak=False)


