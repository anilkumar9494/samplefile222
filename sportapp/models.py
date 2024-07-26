from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models

from dashboard.models import *
from common.models import BaseModel
from .choices import (TemplateTypes)


class Profile(BaseModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.user, self.email_confirmed)


class Country(BaseModel):

    c_id = models.AutoField(primary_key=True)
    countryName = models.CharField(max_length=50)
    alphaTwoCode = models.CharField(max_length=50)
    countryId = models.CharField(max_length=70)
    

    def __str__(self):
        return self.countryName


class Contact(BaseModel):

    c_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=70)
    email = models.CharField(max_length=50)
    cmt = models.CharField(max_length=1000)

    def __str__(self):
        return self.lname

class Emailtemplate(BaseModel):
    
    t_type = models.PositiveIntegerField(default=0, choices=TemplateTypes.CHOICES)
    subject = models.CharField(max_length=100)
    template = models.TextField()

    def __str__(self):
        return "{}".format(self.t_type)


class Register(BaseModel):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    client_id = models.BigIntegerField(default=1001, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    dob = models.DateField(max_length=8)
    verify=models.BooleanField(default=False)
    email = models.CharField(max_length=50, unique=True)
    mob = models.CharField(max_length=13)
    pwd1 = models.CharField(max_length=100)
    pwd2 = models.CharField(max_length=100)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)
    address  = models.CharField(max_length=100)
    pincode = models.IntegerField(null=True,blank=True)
    secondaryemail=models.CharField(max_length=100,null=True,blank=True,default=None)
    reasonsecondaryemail=models.CharField(max_length=500,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True,default=None)
    state  = models.CharField(max_length=100,null=True,blank=True,default=None)
    language = models.CharField(max_length=100,null=True, blank=True)
    ip_address = models.CharField(max_length=100,null=True, blank=True)   # ip-address of the user.
    acc_type = models.ManyToManyField('dashboard.Addaccounttype')
    acc_limit = models.IntegerField(default=4)
    demo_acc_limit = models.IntegerField(default=2)
    c_id = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.fname, self.client_id)


class RegisterUserCampaign(BaseModel):

    register = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True)
    mt4_id = models.BigIntegerField(default=0)
    ref_code = models.BigIntegerField("Ref Code", default=0, null=True, blank=True) # partner code (ClientPortal User.id)
    campaign_code = models.CharField(max_length=100, null=True, blank=True)
    campaign = models.CharField(max_length = 100, null= True, blank = True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.register, self.ref_code)



class Mt4trades(models.Model):

    ticket = models.IntegerField(primary_key=True)
    login = models.IntegerField()
    symbol = models.CharField(max_length=16)
    digits = models.IntegerField()
    cmd = models.IntegerField()
    volume = models.IntegerField()
    open_time = models.DateTimeField()
    open_price = models.FloatField()
    sl = models.FloatField()
    tp = models.FloatField()
    close_time = models.DateTimeField()
    expiration = models.DateTimeField()
    reason = models.IntegerField()
    conv_rate1 = models.FloatField()
    conv_rate2 = models.FloatField()
    commission = models.FloatField()
    commission_agent = models.FloatField()
    swaps = models.FloatField()
    close_price = models.FloatField()
    profit = models.FloatField()
    taxes = models.FloatField()
    comment = models.CharField(max_length=32)
    internal_id = models.IntegerField()
    margin_rate = models.FloatField()
    timestamp = models.IntegerField()
    magic = models.IntegerField()
    gw_volume = models.IntegerField()
    gw_open_price = models.IntegerField()
    gw_close_price = models.IntegerField()
    modify_time = models.DateTimeField()
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'MT4_TRADES'

    def __str__(self):
        return '{}'.format(self.login)


class Mt4users(models.Model):
    
    login = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.CharField(max_length = 50)
    balance = models.FloatField()

    class Meta:
        db_table = "MT4_USERS"

    def __str__(self):
        return str(self.login) + '-' + str(self.name)


class Addpage(models.Model):
   name=models.CharField(max_length=120,null=True)
   def __str__(self):
     return self.name

class Page_Seo(models.Model):
    title=models.TextField(null=True)
    meta_title=models.TextField(null=True)
    meta_description=models.TextField(null=True)
    meta_keyword=models.TextField(null=True)
    og_img=models.ImageField(upload_to ='uploads/og_img') 
    img_alt=models.CharField(max_length=100,null=True)
    canonical_url=models.URLField(max_length = 200,null=True) 
    datetime=models.DateField(auto_now_add=True)
    

    def __str__(self):
       return self.title