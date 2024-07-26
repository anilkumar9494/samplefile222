from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django .urls import reverse

from dashboard.models import Addaccounttype
from dashboard.models import Addcurrency
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View, TemplateView
from django.conf import settings
from django.http import HttpResponse
from .models import DemoAccount,UserWithdraw
from .models import LiveAccount
from django.shortcuts import get_object_or_404
from .models import Uploaddocument,WalletFinance
from django.contrib import auth
from django.core.mail import send_mail
import datetime
from django . core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from sportapp.models import Register
import random, string
from clientportal import jwt_decode
from .jwt_decode import (
    encode_jwt, decode_jwt
)
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . form import *

def make_password(stringLength=15):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

@login_required(login_url='login_client')
def dashboard(request):
    return render(request,'clientportal/dashboard.html')


def profile(request):
    register=Register.objects.filter(user_id=request.user.id)
    return render(request,'clientportal/profile.html',{'r':register})

# def profileupdate(request):
#     if request.method == 'POST':
#         r  = Register.objects.filter(id=request.user.id)
#         email = request.POST['email']
#         reason = request.POST['reason']

#         r.update(secondaryemail=email,reasonsecondaryemail=reason)
#     return redirect(dashboard)

def wallet_finance(request):
    wallet = WalletFinance.objects.filter(list_display=True, user_id=request.user.id).order_by('-id')
    return render(request, 'clientportal/walletfinance.html',{'wallet':wallet})

#
# def upload_document(request):
#     documents = None
#     user = get_object_or_404(User.objects.filter(id=request.user.id))
#     try:
#         documents = get_object_or_404(Uploaddocument.objects.filter(user=user))
#     except:
#         pass
#     print('abhishek',documents)
#     if request.method == 'POST':
#         # u = User.objects.get(id=id)
#         poifront = request.FILES.get('pidentityfront')
#         poiback = request.FILES.get('pidentityback')
#         poafront = request.FILES.get('paddressfront')
#         poaback = request.FILES.get('paddressback')
#         crs = request.FILES.get('paddressfront')
#         odoc = request.FILES.get('paddressback')
#
#         Uploaddocument.objects.create(user_id=request.user.id,poifront=poifront,poiback=poiback,poafront=poafront,poaback=poaback,crs=crs,odoc=odoc)
#         return redirect(dashboard)
#     else:
#         pass
#
#     return render(request,'clientportal/upload_document.html',{'user':user,'documents':documents})


def get_object_or_none(Models, request):
    try:
        obj = Models.objects.get(user=request.user)
        return obj
    except Models.DoesNotExist:
        return None
@login_required(login_url='login_client')
def upload_document(request):
    documents = get_object_or_none(Uploaddocument,request)
    if not documents:
        if request.method == 'POST':
            Uploaddocument.objects.create(
                user=request.user,
                poifront=request.FILES.get('pidentityfront'),
                poiback=request.FILES.get('pidentityback'),
                poafront=request.FILES.get('paddressfront'),
                poaback=request.FILES.get('paddressback'),
                crs=request.FILES.get('crscans'),
                odoc=request.FILES.get('otherdoc')
            )
            return redirect(dashboard)
        return render(request,'clientportal/upload_document.html',{'documents':documents})
    else:
        user_doc = get_object_or_404(Uploaddocument,user=request.user)
        if request.method == 'POST':
            if request.FILES.get('pidentityfront'):
                user_doc.poifront = request.FILES.get('pidentityfront')
            if request.FILES.get('pidentityback'):
                user_doc.poiback = request.FILES.get('pidentityback')
            if request.FILES.get('paddressfront'):
                user_doc.poafront = request.FILES.get('paddressfront')
            if request.FILES.get('paddressback'):
                user_doc.poaback = request.FILES.get('paddressback')
            if request.FILES.get('paddressfront'):
                user_doc.crs = request.FILES.get('paddressfront')
            if request.FILES.get('paddressback'):
                user_doc.odoc = request.FILES.get('paddressback')
            user_doc.save()
            return redirect(dashboard)
        return render(request,'clientportal/edit_document.html',{'user_doc':user_doc})
'''
Forget Password
'''
def forget_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                user = get_object_or_404(User.objects.filter(email=email))
                print('user : ',user)
                print('yes exists')
                message = 'Reset your password'
                subject = 'Reset Password'
                content = ''
                from_mail = '6ibettestmail@gmail.com'
                to_email = str(email)
                print('email',to_email)
                pk = user.pk
                print('user pk :',pk)
                link = request.build_absolute_uri(reverse('reset_password'
                            , kwargs={'pk': pk}))
                context_data = {
                    'username': user.username,
                    'link':link,
                }
                template_name = 'clientportal/forget_password_mail.html'
                text_content = render_to_string(template_name,context=context_data)
                msg  = EmailMultiAlternatives(subject,content,from_mail,[to_email])
                msg.attach_alternative(text_content, "text/html")
                msg.send()
                return redirect('login_client')
            else:
                print('not exists')
        else:
            print(form.errors)
    else:
        form = ResetPasswordForm()
    return render(request,'clientportal/forget_password.html',{'form':form})


def reset_password(request,pk):
    try:
        if User.objects.filter(pk=pk).exists():
            instance = get_object_or_404(User.objects.filter(pk=pk))
    except:
        return render(request,'unauthorized.html',{})

    if request.method == 'POST':
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            password = request.POST.get('new_password1')
            instance.set_password(password)
            instance.save()
            return redirect('login_client')
        else:
            print(form.errors)

    else:
        form = ResetPasswordConfirmForm()
    return render(request,'clientportal/forget_password_confirm.html',{'form':form,'pk':pk})


def changepassword(request):
    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        currentpassword = request.user.password  # user's current password
        form = PasswordChangeForm(user=request.user, data=request.POST)
        currentpasswordentered = request.POST.get('old_password')
        newpasswordentered = request.POST.get('new_password1')
        oldpasswordcheck = check_password(
            currentpasswordentered, currentpassword)
        if oldpasswordcheck:
            if newpasswordentered != currentpasswordentered:
                if form.is_valid():
                    form.save()
                    message = 'The password has been changed successfully'
                    return redirect('login_client')


                else:
                    print(form.errors)
            else:
                message = 'The passwords can not be same as the old one.'
        else:
            message = 'The old password that you enter is wrong.'
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request,'clientportal/changepassword.html',{'message': message, 'form': form})

def logins(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        register = auth.authenticate(username=username,password=password)
        if register is not None:
            auth.login(request,register)
            return redirect(dashboard)
        else:
            return render(request,'login.html',{'error':'Invalid Login Credentials'})
    else:
        context_data={
        'u':User.objects.all()
        }
        return render(request,'login.html',context_data)


def myaccount(request):
    ac = LiveAccount.objects.all()
    return render(request,'clientportal/myaccount.html',{'ac':ac})


class DepositSuccessTemplateView(TemplateView):
    template_name = "clientportal/depositsuccess.html"

class DepositFailureTemplateView(TemplateView):
    template_name = "clientportal/depositfailure.html"


def account_overview(request):
    return render(request,'clientportal/accountoverview.html')

def support(request):
    return render(request,'clientportal/support.html')

def downplat(request):
    return render(request,'clientportal/downplat.html')

def deposit(request):
    return render(request,'clientportal/deposit.html')

def addemail(request):
    if request.method == 'POST':
        r  = Register.objects.filter(user_id=request.user.id)
        email = request.POST['email']
        reason = request.POST['reason']
        r.update(secondaryemail=email,reasonsecondaryemail=reason)

        print(r)
        return redirect(dashboard)
    return render(request,'clientportal/addemail.html')



def deposit_divepay(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositdivepay.html',{'ca':ca})


def deposit_neteller(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositneteller.html',{'ca':ca})


def deposit_skrill(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositskrill.html',{'ca':ca})

def manage_funds(request):
    return render(request,'clientportal/managefunds.html')


def depositfailure(request):
    return render(request, 'clientportal/depositfailure.html')


def bitcoin_payment(request):
    return render(request, 'clientportal/bitcoinpayment.html')

def bitcoin_withdraw(request):
    return render(request, 'clientportal/bitcoin_withdraw.html')


def usdt(request):
    return render(request, 'clientportal/bitcoinpayment.html')

def usdt_withdraw(request):
    return render(request, 'clientportal/usdt_withdraw.html')


def depositsuccess(request):
    return render(request, 'clientportal/usdt.html')


def withdraw(request):
    return render(request,'clientportal/withdraw.html')


def withdraw_divepay(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        w = UserWithdraw(amount = amount, username = username , email = email )
        w.save()
        return redirect(withdraw_divepay)
    return render(request,'clientportal/withdrawdivepay.html')


def send_mail_func(send_to=None, username=None, account_no=None, your_password=None, investor_pass=None, server_type=None,*args, **kwargs):
    data = {
        'user': username.title(),
        'login_account': account_no,
        'pwd': your_password,
        'inpwd': investor_pass,
        'server': server_type,
    }
    msg_text = """Hello {user},
Login : {login_account}
Password: {pwd}
Investor password: {inpwd}
Server: {server}
""".format(**data)
    if send_to and your_password and account_no:
        send_mail("Your Account Details", msg_text, "6ibettestmail@gmail.com", [send_to], fail_silently=False)

def live_account_open_api_call(request_data):
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'
    jwt_dict_data = jwt_decode.dict_data
    jwt_dict_data['server'] = "Real"
    jwt_dict_data['leverage'] = "1000"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.username
    jwt_dict_data['client_email'] = request_data.user.register.email
    #jwt_dict_data['comment'] = "{0},{1}".format(
         #request_data.user.register.registerusercampaign_set.first().campaign_code,
        # request_data.user.register.registerusercampaign_set.first().ref_code
    )
    jwt_dict_data['client_ip'] = request_data.META['REMOTE_ADDR']
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}

@login_required(login_url='login_client')
def laccount(request):
    if request.method == "POST":
        ac = request.POST['acctype']
        ct = request.POST['ctype']
        response_data = live_account_open_api_call(request)
        r_data = response_data['data']
        laccount = LiveAccount(ac_type=ac,cu_type=ct,user_id=request.user.id,account_no=r_data.get('login'))
        laccount.save()
        send_mail_func(
            send_to=r_data.get('email'),
            username=r_data.get('name'),
            account_no=r_data.get('login'),
            your_password=r_data.get('password'),
            investor_pass=r_data.get('investor_pass'),
            server_type=response_data['server'],
        )
        return redirect(dashboard)
    else:
        context_data ={
        'ac':Addaccounttype.objects.all(),
        'ca':Addcurrency.objects.all()
        }
    return render(request,'clientportal/laccount.html',context_data)

@login_required(login_url='login_client')
def demo_account_open_api_call(request_data):
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'
    jwt_dict_data = jwt_decode.dict_data
    jwt_dict_data['server'] = "Demo"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.username
    jwt_dict_data['client_email'] = request_data.user.register.email
    jwt_dict_data['client_ip'] = request_data.META['REMOTE_ADDR']
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}


def daccount(request):
    if request.method == "POST":
        ac = request.POST['accounttype']
        ct = request.POST['ctype']
        response_data = demo_account_open_api_call(request)
        r_data = response_data['data']
        daccount = DemoAccount(ac_type=ac,cu_type=ct,user_id=request.user.id,account_no=r_data.get('login'))
        daccount.save()
        send_mail_func(
            send_to=r_data.get('email'),
            username=r_data.get('name'),
            account_no=r_data.get('login'),
            your_password=r_data.get('password'),
            investor_pass=r_data.get('investor_pass'),
            server_type=response_data['server'],
        )
        return redirect(dashboard)
    else:
        context_data ={
        'ac':Addaccounttype.objects.all(),
        'ca':Addcurrency.objects.all()
        }
    return render(request,'clientportal/daccount.html',context_data)

class GetLiveAccountDetailsView(View):
    def account_detail_url(self, request_data):
        url = "https://demodc.use.6i.nullpoint.io/accountget"
        jwt_dict_data = jwt_decode.live_account_data
        account_no = request_data.user.liveaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, request, *args, **kwargs):
        data = self.account_detail_url(self.request)
        if data['status'] == 0:
            return data['msg']
        print(data)
        # save data and show data.
        return HttpResponse("Live account detail")

class GetDemoAccountDetailsView(View):
    def account_detail_url(self, request_data):
        url = "https://demodc.use.6i.nullpoint.io/accountget"
        jwt_dict_data = jwt_decode.demo_account_data
        account_no = request_data.user.demoaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, request, *args, **kwargs):
        data = self.account_detail_url(self.request)
        if data['status'] == 0:
            return data['msg']
        # save data and show data.
        print(data)
        return HttpResponse("Demo account detail")



def settings(request):
    return render(request,'clientportal/settings.html')
