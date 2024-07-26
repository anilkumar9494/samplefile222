from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

from common.models import BaseModel
from sportapp.models import Register


class DemoAccount(BaseModel):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    account_no = models.BigIntegerField(default=0)
    type = models.SmallIntegerField(default=1, editable=False)
    ac_type  = models.CharField(max_length=300)
    cu_type = models.CharField(max_length=300)
    balance = models.FloatField(default=0)
    equity = models.FloatField(default=0,null=True, blank=True)
    group = models.CharField(max_length=120, default='',null=True, blank=True)  

    def __str__(self):
        return self.ac_type


class LiveAccount(BaseModel):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    account_no = models.BigIntegerField(default=0)
    type = models.SmallIntegerField(default=0, editable=False)
    ac_type  = models.CharField(max_length=300)
    cu_type = models.CharField(max_length=300)
    balance = models.FloatField(default=0)
    equity = models.FloatField(default=0,null=True, blank=True)
    group = models.CharField(max_length=120, default='',null=True, blank=True)
    leverageInCents=models.CharField(max_length=120,null=True, blank=True)
    name = models.CharField(max_length=120, default='',null=True, blank=True)
    lastName=models.CharField(max_length=120,null=True, blank=True)
    description = models.CharField(max_length=120, default='',null=True, blank=True)
    accessRights=models.CharField(max_length=120,null=True, blank=True)
    bonus = models.CharField(max_length=120, default='',null=True, blank=True)
    nonWithdrawableBonus=models.CharField(max_length=120,null=True, blank=True)
    live_account_details=models.TextField()
    def __str__(self):
        return str(self.user)


def user_upload_document(instance, filename):
    return "images/{}/{}".format(instance.user_id, filename)


class Uploaddocument(BaseModel):

    type = (
        (1, 'Pending Approval'),
        (2, 'Approved'),
    )

    status_choices = (
        (1, 'Not uploaded'),
        (2, 'Uploaded'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    poifront = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    poiback = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    poafront = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    poaback = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    crs = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    odoc = models.FileField(upload_to=user_upload_document, null=True, blank=True,default=None)
    type = models.IntegerField(default=1, choices=type)
    status = models.IntegerField(default=1, choices=status_choices)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user, self.approve)


class LiveAcAmount(BaseModel):

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	liveaccount = models.OneToOneField(LiveAccount, on_delete=models.SET_NULL, null=True)
	amount = models.FloatField(default=0)

	def __self__(self):
		return "{} {} {}".format(self.user, self.liveaccount, self.amount)


class DemoAcAmount(BaseModel):

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	demoaccount = models.OneToOneField(DemoAccount, on_delete=models.SET_NULL, null=True)
	amount = models.FloatField(default=0)

	def __self__(self):
		return "{} {} {}".format(self.user, self.demoaccount, self.amount)


class UserWallet(BaseModel):

    status_choices = (
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('R', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    register = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    w_id = models.BigIntegerField(default=0, null=True, blank=True)
    # status = models.CharField(max_length=1, choices=status_choices, default='A')

    def __str__(self):
        return "{0}".format(self.user)

    def save(self, *args, **kwargs):
        self.w_id = self.id
        super(UserWallet, self).save(*args, **kwargs)


class WalletFinance(BaseModel):

    type_choice = (
        (0, 'Deposit'),
        (1, 'Transfer IN'),
        (2, 'Transfer OUT'),
    )
    status_choice = (
        (0, 'Processed'),
        (1, 'Not processed'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    t_id = models.CharField("T. Id", max_length=255, blank=True, null=True, editable=True)
    client_id = models.BigIntegerField("Client ID", default=0)
    type = models.IntegerField(default=0, choices=type_choice)
    name = models.CharField("Name", max_length=255)
    country = models.CharField('Country', max_length=255)
    # currency = models.CharField("Currency", max_length=255)
    t_ip = models.GenericIPAddressField("T. IP")
    t_country = models.CharField("T. Country", max_length=255,blank=True, null=True)
    details = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=100)
    feededucted = models.FloatField(default=0, null=True, blank=True)
    status = models.IntegerField(default=0, choices=status_choice)
    list_display = models.BooleanField("Only For Deposit", default=True)

    def __str__(self):
        return "{0}".format(self.user)

    def save(self, *args, **kwargs):
        self.t_id = "6bd{0}".format(self.id)
        super(WalletFinance, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']


class UserDeposits(BaseModel):

    action_choice = (
        (0, 'Pending'),
        (1, 'Not Approve'),
        (2, 'Approve'),
        (3, 'Try'),
    )

    walletfinance = models.ForeignKey(WalletFinance, on_delete=models.SET_NULL, null=True)
    comment = models.TextField("Commnet (Remark)")
    item_id = models.CharField("Item Id", max_length=255)
    batch = models.CharField("Batch Id", max_length=255, blank=True, null=True)
    action_choice = models.IntegerField(default=0, choices=action_choice)

    def __str__(self):
        return '{0} {1}'.format(self.walletfinance, self.action_choice)

    class Meta:
        ordering = ['id']


class UserDepositApproval(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approve = models.BooleanField(default=True)

    def __str__(self):
        return "{0} {1}".format(self.user, self.approve)

    class Meta:
        ordering = ['id']


class UserWithdraw(BaseModel):

    status_choices = (
        (0, 'Pending'),
        (1, 'Approve'),
        (2, 'Not Approve'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    t_id = models.CharField("T. Id", max_length=255, blank=True, null=True, editable=True)
    client_id = models.BigIntegerField("Client ID", default=0)
    name = models.CharField("Name", max_length=255)
    country = models.CharField('Country', max_length=255)
    currency = models.CharField("Currency", max_length=255)
    t_ip = models.GenericIPAddressField("T. IP")
    t_country = models.CharField("T. Country", max_length=255,blank=True, null=True)
    details = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=100)
    amount = models.FloatField()
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    status = models.IntegerField(default=0, choices=status_choices)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.t_id = "6bw{0}".format(self.id)
        super(UserWithdraw, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']


class Client_Commission(BaseModel):

    register = models.ForeignKey(Register,on_delete=models.CASCADE)
    mt4_account_no = models.BigIntegerField()
    volume = models.FloatField()
    commision_paid = models.FloatField(default=0.00)
    commision_unpaid = models.FloatField(default=0.00)
    wallet = models.FloatField(default=0.00)

    def __str__(self):
        return str(self.register)

class Positions(models.Model):
    login_account = models.CharField(max_length=255,null=True,blank=True)
    positionId = models.CharField(max_length=255,null=True,blank=True)
    entryPrice = models.CharField(max_length=255,null=True,blank=True)
    direction = models.CharField(max_length=255,null=True,blank=True)
    volume = models.CharField(max_length=255,null=True,blank=True)
    Profit = models.CharField(max_length=255,null=True,blank=True)
    closePrice = models.CharField(max_length=255,null=True,blank=True)
    symbol = models.CharField(max_length=255,null=True,blank=True)
    commission = models.CharField(max_length=255,null=True,blank=True)
    openTimestamp = models.CharField(max_length=255,null=True,blank=True)
    closeTimestamp = models.CharField(max_length=255,null=True,blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    client_id=models.CharField(max_length=255,null=True,blank=True)
    action = models.CharField(max_length=255)
    swap = models.CharField(max_length=255,null=True,blank=True)
    bookType = models.CharField(max_length=255,null=True,blank=True)
    stake = models.CharField(max_length=255,null=True,blank=True)
    spreadBetting = models.CharField(max_length=255,null=True,blank=True)
    usedMargin = models.CharField(max_length=255,null=True,blank=True)
    trade_type = models.CharField(max_length=255,null=True,blank=True)
    pnl= models.CharField(max_length=255,null=True,blank=True)
    depositConversionRate= models.CharField(max_length=255,null=True,blank=True)
    usdConversionRate= models.CharField(max_length=255,null=True,blank=True)
    dealId= models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return '{0}'.format(self.client_id)

    class Meta:
        ordering = ['id']
