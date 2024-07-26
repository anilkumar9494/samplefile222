from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel
from sportapp.models import Register


class Securityque(BaseModel):

    name  = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Addaccounttype(BaseModel):

    name  = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Addcurrency(BaseModel):

    name  = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Adddepartment(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Addoffice(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Addbrand(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Addleadsregions(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Addsalesnotes(BaseModel):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=1000, null=True, blank=True)
    client_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.note


class Leads_access_level(BaseModel):

    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Access_level(BaseModel):

    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Depositpaymentgetway(BaseModel):

    '''
    type: 0 => Deposit
    type: 1 => Transfer IN
    type: 2 => Transfer OUT
    '''

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    trans_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    fees = models.FloatField()
    amount = models.FloatField()
    type = models.SmallIntegerField(default=0)
    total_amount = models.FloatField()
    currency = models.CharField(max_length=100)
    additional_message = models.CharField(max_length=200)
    member = models.CharField(max_length=100)
    buyer = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    tawkuuid = models.CharField(max_length=500)
    phpsessid = models.CharField(max_length=500)

    def __str__(self):
        return self.member


class Agentusercreate(BaseModel):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    office = models.CharField(max_length=100)
    brandvisibility = models.CharField(max_length=100)
    accesslevel = models.CharField(max_length=100)
    leadsaccesslevel = models.CharField(max_length=100)
    leadsregions = models.CharField(max_length=1000)
    password = models.CharField(max_length=100)
    confirmpassword = models.CharField(max_length=100)

    def __str__(self):

        if self.firstname:
            return self.firstname
        return ""


class Comments(BaseModel):

    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name


class Transaction_Method(BaseModel):

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    type=models.CharField(max_length=100)
    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
    amount=models.FloatField()
    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
    batch_number=models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-id',)


class transaction_ibmethod_mdl(BaseModel):

    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    client_id = models.BigIntegerField(null=True,blank=True)
    type=models.CharField(max_length=100)
    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
    amount=models.FloatField()
    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
    batch_number=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class SalesQueue(BaseModel):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SalesAssignment(BaseModel):
    
    agent = models.OneToOneField(Agentusercreate, on_delete=models.CASCADE)
    enabled_state = models.BooleanField(null=True, blank=True)
    default_state = models.BooleanField(null=True, blank=True)
    country_list = models.CharField(max_length=255, null=True, blank=True)
    sales_queues = models.ForeignKey(SalesQueue, on_delete=models.CASCADE, null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.agent.firstname


#class Transaction_Ib_Method(BaseModel):
#    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
#    type=models.CharField(max_length=100)
#    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
#    amount=models.FloatField()
#    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
#    batch_number=models.CharField(max_length=100)
#
#    def __str__(self):
#        return self.user.username
#
# class Transaction_IbMethod(BaseModel):
#     id = models.AutoField(primary_key=True)
#     user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
#     client_id = models.BigIntegerField(null=True,blank=True)
#     type=models.CharField(max_length=100)
#     comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
#     amount=models.FloatField()
#     currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
#     batch_number=models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.user.username





class BlogCategory(models.Model):
    name=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    slug=models.SlugField(default="", null=False)

    img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    datetime=models.DateField(auto_now_add=True)
    

    def __str__(self):
       return self.name




class BlogSubCategory(models.Model):
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    slug=models.SlugField(default="", null=False)

    img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    datetime=models.DateField(auto_now_add=True)
    

    def __str__(self):
       return self.name





class Blog(models.Model):
    BLOG_STATUS = ((0, 'Pending'), (1, 'Published'), (2, 'Rejected'))
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    blog_subcategory = models.ForeignKey(BlogSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=100,null=True)
    short_desc=models.TextField(null=True)

    description=models.TextField(null=True,blank=True)
    slug=models.SlugField(default="", null=False)

    img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    datetime=models.DateField(auto_now_add=True)
    status = models.SmallIntegerField(choices=BLOG_STATUS)

    def __str__(self):
       return self.title






class Blog_Seo(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    title=models.TextField(null=True)
    meta_title=models.TextField(null=True)
    meta_description=models.TextField(null=True)
    meta_keyword=models.TextField(null=True)
    og_img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    canonical_url=models.URLField(max_length = 200,null=True) 
    datetime=models.DateField(auto_now_add=True)

    def __str__(self):
       return self.title



class BlogCategory_Seo(models.Model):
    blog = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    title=models.TextField(null=True)
    meta_title=models.TextField(null=True)
    meta_description=models.TextField(null=True)
    meta_keyword=models.TextField(null=True)
    og_img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    canonical_url=models.URLField(max_length = 200,null=True) 
    datetime=models.DateField(auto_now_add=True)

    def __str__(self):
       return self.title




class BlogSubCategory_Seo(models.Model):
    blog = models.ForeignKey(BlogSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    title=models.TextField(null=True)
    meta_title=models.TextField(null=True)
    meta_description=models.TextField(null=True)
    meta_keyword=models.TextField(null=True)
    og_img=models.ImageField(upload_to ='uploads/og_img') 
    image_caption=models.CharField(max_length=100,null=True)
    canonical_url=models.URLField(max_length = 200,null=True) 
    datetime=models.DateField(auto_now_add=True)

    def __str__(self):
       return self.title
