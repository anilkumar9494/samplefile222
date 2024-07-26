from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.views.generic import View, TemplateView
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.db import connection
from django.db.models import Sum
from django.utils import translation
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django . core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import random, string
import datetime
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
from pandas import Series, DataFrame

from dashboard.models import *
from dashboard.filters import DateRangeMaker
from dashboard.views import exportData
from clientportal import jwt_decode
from clientportal.models import *
from sportapp.models import *
from .models import *
from .form import *
from .jwt_decode import (encode_jwt, decode_jwt)
import json
import requests

def edit_mt4_account_api_call(request_data):

    url = 'https://demodc.use.6i.nullpoint.io/accountedit/'
    jwt_dict_data = jwt_decode.edit_account
    jwt_dict_data['account'] = request_data['account']
    # jwt_dict_data['comment'] = "{0},{1}".format(
    #          request_data['campaignCode'],
    #          request_data['ibId']
    #     )

    encoded_return_data = "request_message={0}".format(jwt_decode.encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": jwt_decode.decode_jwt(data=response_api.text)}

def country_api_call(request_data):

    import requests
    
    url = "https://live-six.divsolution.com/Country_List"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    country_list=json.loads(response.text).get('countries')
    print("=============",len(json.loads(response.text).get('countries')))
    for country in country_list:
        print("======country=======",country['country']['countryName'])
        Country.objects.create(countryName=country['country']['countryName'],alphaTwoCode=country['country']['alphaTwoCode'],
                                countryId=country['country']['countryId'],c_id=country['country']['countryId'])
    return JsonResponse({"data": json.loads(response.text)})

from datetime import datetime, date
@login_required(login_url='login_client')
def client_dash(request):

    today = date.today()
    context = {}
    free_margin, logins, profit_list, list_flat, graph_list, set_list = [], [], [], [], [], []
    open_pro_list, flat_list, profitability_list, final_list, final_list_2 = [], [], [], [], []
    cls_comm_list, cls_comm_sum_list, comm_trades_list, open_com_lst = [], [], [], []
    swaps_in_cls, cls_swap_lst, swaps_in_opn = [], [], []

    #############  for margin free #########

    _data = f'https://www.6imarkets.com/api/v1/live_accounts/{request.user.id}/'
    
    get_data = requests.get(_data).json()
    print("============get_data==",get_data)
    for data in get_data['data']:
        try:
            if data['login']:
                logins.append(data['login'])
                free_margin.append(data['margin_free'])
        except:
            pass

    for i in range(0, len(free_margin)):
        free_margin[i] = float(free_margin[i])

    context['free_margin'] = round(sum(free_margin), 2)
    profit_list=[]
    #############  margin free ends  #########

    # with connection.cursor() as cursor:
        # for log in logins:
            # cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
            # data_sql = cursor.fetchall()

            # for data in data_sql:
                # data_list = list(data)
                # profit_list.append(data_list)
                
            # cursor.execute(f"select MT4_TRADES.COMMISSION from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
            # close_comm = cursor.fetchall()
            # for comm in close_comm:
                # cls_comm_lis = list(comm)
                # cls_comm_list.append(cls_comm_lis)
            
            # cursor.execute(f"select MT4_TRADES.SWAPS from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
            # cls_swaps = cursor.fetchall()
            # for swaps in cls_swaps:
                # cls_swaps_list = list(swaps)
                # swaps_in_cls.append(cls_swaps_list)

            # cursor.execute(f"select MT4_TRADES.SYMBOL from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
            # graph_response = cursor.fetchall()

            # for response in graph_response:
                # for graph in response:
                    # graph_list.append(graph)

            # cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%' ")
            # open_pro = cursor.fetchall()

            # for pro in open_pro:
                # pro_list = list(pro)
                # open_pro_list.append(pro_list)

            # cursor.execute(f"select MT4_TRADES.COMMISSION from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%' ")
            # open_comm_pro = cursor.fetchall()

            # for open_comm in open_comm_pro:
                # open_comm_list = list(open_comm)
                # open_com_lst.append(open_comm_list)
            
            # cursor.execute(f"select MT4_TRADES.SWAPS from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%' ")
            # opn_swaps = cursor.fetchall()

            # for swaps in opn_swaps:
                # opn_swaps_list = list(swaps)
                # swaps_in_opn.append(opn_swaps_list)

            # cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
            # proftablity_data = cursor.fetchall()

            # for ability in proftablity_data:
                # lists_data = list(ability)
                # profitability_list.append(lists_data)
    
    #############  for closing p&l ########### 
    
    for i in range(len(profit_list)):
        for j in range(len(profit_list[i])):
            list_flat.append(profit_list[i][j])

    for i in range(len(cls_comm_list)):
        for j in range(len(cls_comm_list[i])):
            cls_comm_sum_list.append(cls_comm_list[i][j])

    for i in range(len(swaps_in_cls)):
        for j in range(len(swaps_in_cls[i])):
            cls_swap_lst.append(swaps_in_cls[i][j])

    pl_with_comm = sum(cls_comm_sum_list)+sum(list_flat)+sum(cls_swap_lst)

    if profit_list and cls_comm_sum_list:
        context['closing_p_l'] = round(pl_with_comm, 2)
    else:
        pass

    ############# closing p&l ends ###########

    #############  for profitability ###########

    for i in range(len(profitability_list)):
        for j in range(len(profitability_list[i])):
            final_list.append(profitability_list[i][j])

    for pro in final_list:
        if pro > 0:
            final_list_2.append(pro)

    if profitability_list:
        context['profitability'] = round((len(final_list_2)/len(profitability_list))*100, 2)
    else:
        pass

    ############# profitability ends ###########

    #############  for open p&l ###########

    flat_list = [item for open_pro in open_pro_list for item in open_pro]

    final_flat_list = [item for open_pro in open_com_lst for item in open_pro]

    final_swpas_list = [item for open_pro in swaps_in_opn for item in open_pro]

    open_comm_with_pl = sum(final_flat_list)+sum(flat_list)+sum(final_swpas_list)

    if open_pro_list and open_com_lst:
        context['open_p_l'] = round(open_comm_with_pl, 2)
    else:
        pass

    ############# open p&l ends ###########

    ############# Graph data starts ###########

    for crypto in graph_list:
        graph_list.count(crypto)
        set_list.extend([crypto, graph_list.count(crypto)])

    res_dct = {set_list[i]: set_list[i + 1] for i in range(0, len(set_list), 2)}
    key_data, values_data, values_graph_data, list_graph_val = [], [], [], []

    for key, value in res_dct.items():
        key=key.replace('-','')
        key_data.append(key)
        values_data.append(value)

    for values in values_data:
        values_to_append = round((values/sum(values_data))*100, 2)
        values_graph_data.append(values_to_append)

    context['values_graph_data'] = values_graph_data
    context['key_data'] = key_data

    ############# Graph data ends ###########
    obj=LiveAccount.objects.filter(user=request.user)
    context['live_ac'] = obj
    
    return render(request, 'clientportal/dashboard.html', context=context)


@login_required(login_url='login_client')
def profile(request, lang=None):

    # admin_user = User.objects.all().filter(is_superuser=True)[0]
    register = Register.objects.filter(user_id=request.user.id)
    year_val = ''
    month_val = ''
    date_val = ''
    dob_year = ''
    dob_month = ''
    dob_date = ''
    secondary_email_val = ''

    for i in register:
        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        dob_datesplit = str(i.dob).split('-')
        dob_year = dob_datesplit[0]
        dob_month = dob_datesplit[1]
        dob_date = dob_datesplit[2]

        if i.secondaryemail == None:
            secondary_email_val = 'No Email'
        else:
            secondary_email_val = i.secondaryemail

    return render(request, 'clientportal/profile.html', {
        'r': register,
        'added_on_year_val': year_val,
        'added_on_month_val': month_val,
        'added_on_date_val': date_val,
        'secondary_email_val': secondary_email_val,
        'dob_year':dob_year,
        'dob_month':dob_month,
        'dob_date':dob_date,
    })


@login_required(login_url='login_client')
def wallet_finance(request, exporttype=None):
    
    wallet = WalletFinance.objects.filter(list_display=True, user_id=request.user.id).order_by('-id')
    transaction = Transaction_Method.objects.filter(user_id=request.user.id).order_by('-id')

    response_list = []

    year_val = ''
    month_val = ''
    date_val = ''
    id = ''
    type = ''
    amount = ''
    currency = ''
    comments = ''
    status = ''
    transfer_to = ''
    transfer_in = ''
    transfer_type = ''
    get_status_display = ''

    if not request.GET.get('added_on'):
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            try:
                comments = i.comments.name
            except:
                comments = ''

            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'added_on':i.added_on,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:

            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))

    elif request.GET.get('added_on') and int(request.GET.get('added_on')) != 7:
        d= DateRangeMaker()
        value = d.change(int(request.GET.get('added_on')))
        transaction = transaction.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            try:
                comments = i.comments.name
            except:
                comments = ''

            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'added_on':i.added_on,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))
    
    elif request.GET.get('added_on') and int(request.GET.get('added_on')) == 7:

        transaction = transaction.filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            try:
                comments = i.comments.name
            except:
                comments = ''

            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'added_on':i.added_on,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))

    response_data = [d[1] for d in sorted(response_list, key=lambda x:x[0])]
    if exporttype:
        response_list = []
        title_headers = ["Date", "Description", "Amount", "Currency", "Status"]
        for rd in response_data:
            dt = f"{rd['added_on_date_val']}-{rd['added_on_month_val']}-{rd['added_on_year_val']}"
            if rd.get('type'):
                details = f"{rd['transfer_type']}-{rd['transfer_to']}"
            else:
                details = f"{rd['transfer_type']}-{rd['comments']}"
            amt = rd['amount']
            curr = rd['currency']
            status = rd['get_status_display']
            response_list.append([dt, details, amt, curr, status])
        return exportData(response_list, exporttype, 'finance', title_headers)
    else:
        return render(request, 'clientportal/walletfinance.html',{
            'response_list':response_data
        })


def get_object_or_none(Models, request):
    
    try:
        obj = Models.objects.get(user=request.user)
        return obj
    except Models.DoesNotExist:
        return None


@login_required(login_url='login_client')
def upload_document(request):

    documents = get_object_or_none(Uploaddocument, request)
    if not documents:
        if request.method == 'POST':
            docs = Uploaddocument.objects.create(
                user=request.user,
                poifront=request.FILES.get('pidentityfront'),
                poiback=request.FILES.get('pidentityback'),
                poafront=request.FILES.get('paddressfront'),
                poaback=request.FILES.get('paddressback'),
                crs=request.FILES.get('crscans'),
                odoc=request.FILES.get('otherdoc')
            )
            docs.status=2
            docs.save()
            # return redirect('dashboard')
        return render(request,'clientportal/edit_document.html',{'documents':documents})
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
            if request.FILES.get('crscans'):
                user_doc.crs = request.FILES.get('crscans')
            if request.FILES.get('otherdoc'):
                user_doc.odoc = request.FILES.get('otherdoc')
            user_doc.status=2
            user_doc.save()
            # return redirect('profile')
        return render(request,'clientportal/edit_document.html',{'user_doc':user_doc,'documents':documents})


def forget_password(request):

    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except:
            user = False

        if user:
            request.session['email'] = user.email
            request.session['username'] = user.username
            otp = random.randint(1000, 99999)
            print("OTP----------------for reset password", otp)
            request.session['otp'] = otp
            # request.session.set_expiry(5000)
            subject = 'OTP Requested for forgotten password'
            message = "We received a forgot password request from your account.\nMake sure not to share your OTP with anyone.\n OTP :{}.\n\n\nplease verify your account if it's not you".format(str(otp))
            from_email = 'support@hme158.com'
            send_mail(subject, message, from_email,
                      [email], fail_silently=False)
            return redirect('otp')
        else:
            messages.error(request, 'Enter a valid Registered Email..!')

    return render(request,'clientportal/forget_password.html')


def otp(request):

    message = ''
    if request.method == 'POST':
        otp = request.POST['otp']
        # if request.session['otp']:
        if int(request.session['otp']) == int(otp):
            return redirect('reset_password')
        else:
            messages.error(request, 'Your otp expired or')
            messages.error(request, 'invalid OTP, try again')
            return redirect('otp')
    return render(request, 'clientportal/otp.html', {'message':message})


def reset_password(request):

    rocks12 = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        email = rocks12.email
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            rocks12.set_password(password)
            rocks12.save()
            subject = request.session['username'].capitalize(
            ) + "Your Password reset"
            message = 'Please find your account details below with credentials after password reset \nEmail :{}\nUser Name :{}\nPassword :{}'.format(
                email.lower(), request.session['username'], str(password))
            from_email = 'support@hme158.com'
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
            )
            return redirect('login_client')
        else:
            messages.error(request, 'password mis match')

    return render(request,'clientportal/forget_password_confirm.html')


def changepassword(request):

    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        currentpassword = request.user.password  # user's current password
        form = PasswordChangeForm(user=request.user, data=request.POST)
        currentpasswordentered = request.POST.get('old_password')
        newpasswordentered = request.POST.get('new_password1')
        oldpasswordcheck = check_password(currentpasswordentered, currentpassword)
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
        register = auth.authenticate(username=username, password=password)

        if register is not None:
            auth.login(request,register)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error':'Invalid Login Credentials'})
    else:
        context_data={
            'u':User.objects.all()
        }
        return render(request, 'login.html', context_data)


@login_required(login_url='login_client')
def myaccount(request):
    obj=LiveAccount.objects.filter(user=request.user)
    dict_live_ac={
        "live_ac":obj
    }
    return render(request,'clientportal/myaccount.html',dict_live_ac)


class DepositSuccessTemplateView(TemplateView):
    template_name = "clientportal/depositsuccess.html"


class DepositFailureTemplateView(TemplateView):
    template_name = "clientportal/depositfailure.html"


@login_required(login_url='login_client')
def account_overview(request):

    context = {}
    duration = ''
    sell_max = ''
    buy_max = ''
    sell_min = ''
    buy_min = ''
    avg_win = ''
    avg_loss = ''
    best_trade_value = ''
    worst_trade_value = ''
    response_list, vol_list, profit_list, withdraw_list, deposit_list = [], [], [], [], []
    gp_list, gl_list, close_tme, open_tme, buy_points_list, sell_point_list = [], [], [], [], [], []
    profit_trades_list, loss_trades_list, avg_pro_list, avg_loss_list, graph_list = [], [], [], [], []
    profttradesinsell, profttradesinbuy, best_worst_trade, all_list, open_pro_list=[], [], [], [], []
    open_posit_list = []

    account_no = request.GET.get('account')
    with connection.cursor() as cursor:
        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
        data_sql = cursor.fetchall()

        # 1-volume, 2-profit, 3-open_time, 4-close_time, 5-ticket, 6-symbol, 7-open_price, 8-close_price, 9-commission, 10-swaps, 11-cmd

        for data in data_sql:
            data_list = list(data)
            all_list.append(data)
            vol_list.append(data_list[0])
            profit_list.append(data_list[1])

            open_tme.append(data_list[2])
            close_tme.append(data_list[3])

            gross_values = data_list[1]
            if str(gross_values).startswith('-'):
                values = str(gross_values).replace("-", "")
                gl_list.append(float(values))
            else:
                gp_list.append(gross_values)

        for pro in profit_list:
            if pro > 0:
                profit_trades_list.append(pro)
            else:
                loss_trades_list.append(pro)

        gross_profit = sum(gp_list)
        gross_loss = sum(gl_list)

        if gross_profit:
            profit_factor = round((gross_profit/gross_loss), 2)
        else:
            profit_factor = 0

        if close_tme:
            if close_tme[-1] >= open_tme[-1]:
                duration = close_tme[-1] - open_tme[-1]
            else:
                duration = 0
        else:
            pass

# -------------

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")
        open_positions_data = cursor.fetchall()

        for open_positions in open_positions_data:
            position_list = list(open_positions)
            open_posit_list.append(position_list)

# -------------
        cursor.execute(f"select MT4_TRADES.SYMBOL from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        graph_response = cursor.fetchall()

        for response in graph_response:
            for graph in response:
                graph_list.append(graph)

        set_list = []
        for crypto in graph_list:
            graph_list.count(crypto)
            set_list.extend([crypto, graph_list.count(crypto)])

        res_dct = {set_list[i]: set_list[i + 1] for i in range(0, len(set_list), 2)}

        key_data = []
        values_data = []
        values_graph_data = []
        list_graph_val = []

        for key, value in res_dct.items():
            key=key.replace('-','')
            key_data.append(key)
            values_data.append(value)

        for values in values_data:
            value_append = round((values/len(values_data))*100, 2)
            values_graph_data.append(value_append)

        cursor.execute(f"select MT4_TRADES.PROFIT, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        average_points_data = cursor.fetchall()

        for average in list(average_points_data):
            if str(average[0]).startswith('-'):
                if average[1].startswith('X'):
                    avg_loss = (average[2]-average[3])*100
                else:
                    avg_loss = (average[2]-average[3])*100000
                avg_loss_list.append(avg_loss)
            else:
                if average[1].startswith('X'):
                    avg_pro = (average[2]-average[3])*100
                else:
                    avg_pro = (average[2]-average[3])*100000
                avg_pro_list.append(avg_pro)

        if profit_trades_list:
            avg_win = sum(avg_pro_list)/len(profit_trades_list)
        else:
            pass

        if loss_trades_list:
            avg_loss = sum(avg_loss_list)/len(loss_trades_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.CMD = '1' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        _1_cmd_data = cursor.fetchall()

        for cmd_1 in _1_cmd_data:
            if cmd_1[5].startswith('X'):
                fi_val = (cmd_1[7]-cmd_1[6])*100
            else:
                fi_val = (cmd_1[7]-cmd_1[6])*100000
            sell_point_list.append(fi_val)

            if str(cmd_1[1]).startswith('-'):
                pass
            else:
                profttradesinsell.append(cmd_1[1])

        if sell_point_list:
            sell_max = max(sell_point_list)
            sell_min = min(sell_point_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.CMD = '0' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        _0_cmd_data = cursor.fetchall()
        
        for cmd_0 in _0_cmd_data:
            if cmd_0[5].startswith('X'):
                final_val = (cmd_0[7]-cmd_0[6])*100
            else:
                final_val = (cmd_0[7]-cmd_0[6])*100000
            buy_points_list.append(final_val)

            if str(cmd_0[1]).startswith('-'):
                    pass
            else:
                profttradesinbuy.append(cmd_0[1])

        if buy_points_list:
            buy_max = max(buy_points_list)
            buy_min = min(buy_points_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.SYMBOL = '' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        withdarw = cursor.fetchall()

        for withdr in withdarw:
            withdra_list = list(withdr)
            withd_amt = withdra_list[0]
            if str(withd_amt).startswith('-'):
                number = str(withd_amt).replace("-", "")
                withdraw_list.append(float(number))
            else:
                deposit_list.append(withd_amt)

        cursor.execute(f"select MT4_TRADES.PROFIT from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME not like '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        proft_best_worst = cursor.fetchall()

        for profit in proft_best_worst:
            profit_list = list(profit)
            best_worst_trade.append(profit_list[0])

        if best_worst_trade:
            worst_trade_value = min(best_worst_trade)
            best_trade_value = max(best_worst_trade)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.PROFIT from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%HANMENGHUI (XUZHOU)%'")

        open_pro = cursor.fetchall()

        for pro in open_pro:
            pro_list = list(pro)
            open_pro_list.append(pro_list)

    total_points = sum(buy_points_list)+sum(sell_point_list)

    if sell_max > buy_max:
        best_trade = sell_max
    else:
        best_trade = buy_max

    if sell_min > buy_min:
        worst_trade = buy_min
    else:
        worst_trade = sell_min

    context['key_data'] = key_data
    context['values_graph_data'] = values_graph_data
    context['closed_positions'] = all_list
    context['open_positions'] = open_posit_list
    context['best_trade_value'] = best_trade_value
    context['worst_trade_value'] = worst_trade_value

    if _0_cmd_data:
        context['profitable_long_trades'] = len(profttradesinbuy)/len(_0_cmd_data)*100
    else:
        pass

    if _1_cmd_data:
        context['profitable_short_trades'] = len(profttradesinsell)/len(_1_cmd_data)*100
    else:
        pass

    context['avg_win'] = avg_win
    context['avg_loss'] = avg_loss

    if data_sql:
        context['profitability'] = (len(profit_trades_list)/len(data_sql))*100
    else:
        pass

    flat_list = [item for open_pro in open_pro_list for item in open_pro]

    if open_pro_list:
        context['open_p_l'] = round(sum(flat_list), 2)
    else:
        pass

    context['total_points'] = total_points
    context['profit_factor'] = profit_factor
    context['total_volume'] = sum(vol_list)
    context['close_p_l'] = sum(profit_list)
    context['total_trades'] = len(data_sql)

    context['avg_order_duration'] = duration

    context['total_deposit'] = sum(deposit_list)
    context['wallet_withdrawls'] = sum(withdraw_list)
    context['best_trade_points'] = best_trade
    context['worst_trade_points'] = worst_trade

    oview_data = f'https://www.6imarkets.com/api/v1/live_accounts/{request.user.id}/'
    get_overview_data = requests.get(oview_data).json()
    for data in get_overview_data['data']:
        try:
            if data['login'] == account_no:
                context['acc_no'] = data['login']
                context['balance'] = data['balance']
                context['equity'] = data['equity']
                context['margin'] = data['margin']
                context['free_margin'] = data['margin_free']
                context['margin_level'] = data['margin_level']
                date_split = data['added_on'].split('T')[0]
                context['added_on'] = date_split
        except:
            pass

    wallet = WalletFinance.objects.filter(list_display=True, user_id=request.user.id).order_by('-id')
    transaction = Transaction_Method.objects.filter(user_id=request.user.id).order_by('-id')

    for i in transaction:

        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        id = i.id
        t = i.type
        amount = i.amount
        currency = i.currency
        try:
            comments = i.comments.name
        except:
            comments = ''

        if comments == "Virtual currency":
            currency_type = "Crypto"
        else:
            currency_type = "USDT"
        if t == '1':
            transfer_type = "Deposit"
        else:
            transfer_type = "Withdrawal"
        response_list.append((year_val+month_val+date_val, {
            'added_on_year_val': year_val,
            'added_on_month_val': month_val,
            'added_on_date_val': date_val,
            'id':id,
            'added_on':i.added_on,
            'transfer_type':transfer_type,
            'currency':"usd",
            'comments':comments,
            'amount':amount,
            'get_status_display':"Completed"
        }))

    for i in wallet:

        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]

        if i.type == 1:
            transfer_type = 'Deposit'
            type = 'Transfer IN'
        elif i.type == 2:
            transfer_type = 'Withdrawal'
            type = 'Transfer OUT'

        if i.details.startswith('Transfer from'):
            transfer_to = i.details.replace('Transfer from','')
        elif i.details.startswith('Transfer to'):
            transfer_to = i.details.replace('Transfer to','')
        elif i.details.startswith('Transfer Out'):
            transfer_to = i.details.replace('Transfer Out','')
        elif i.details.startswith('Transfer IN'):
            transfer_to = i.details.replace('Transfer IN','')
        if i.status == 0:
            get_status_display = 'Completed'
        elif  i.status == 1:
            get_status_display = 'Not Processed'
        if i.currency == 'USD':
            currency = 'usd'

        response_list.append((year_val+month_val+date_val, {
            'wallet':wallet,
            'amount':round(i.amount, 2),
            'type':type,
            'added_on':i.added_on,
            'currency':currency.upper(),
            'get_status_display':get_status_display,
            'added_on_year_val': year_val,
            'added_on_month_val': month_val,
            'added_on_date_val': date_val,
            'transfer_to':transfer_to,
            'transfer_type':transfer_type
        }))

    response_data = [d[1] for d in sorted(response_list, key=lambda x:x[0])]
    context['response_list'] = response_data

    return render(request,'clientportal/accountoverview.html', context=context)


def open_position(request):
    return render(request, 'clientportal/open_position.html', context=context)


def support(request):
    return render(request,'clientportal/support.html')


@login_required(login_url='login_client')
def downplat(request):
    return render(request,'clientportal/downplat.html')




@login_required(login_url='login_client')
def addemail(request):

    to_email = ''
    admin_user = User.objects.all().filter(is_superuser=True)[0]

    if request.method == 'POST':
        r  = Register.objects.filter(user_id=request.user.id)
        previous_sec_email = r[0].secondaryemail
        secondary_email = request.POST['email']
        reason = request.POST['reason']

        if not r[0].email == secondary_email and not r[0].secondaryemail == secondary_email:
            r.update(secondaryemail=secondary_email, reasonsecondaryemail=reason)
            subject = "The User Added/Updated secondary Email"

            body = "The Updated Details are: \n\n"\
                "Client ID: \t{}".format(r[0].client_id)+'\n'+\
                "User: \t\t{}".format(r[0].uname.upper())+'\n'+\
                "Primary Email: {}".format(r[0].email)+'\n'+\
                "Previous secondary email: {}".format(previous_sec_email)+'\n'+\
                "Updated secondary email: {}".format(secondary_email)

            from_email = 'support@hme158.com'
            if admin_user.email:
                to_email = admin_user.email
            else:
                to_email = from_email

            send_mail(
                subject,
                body,
                from_email,
                [to_email],
                fail_silently=False,
            )
            return redirect('profile')
        else:
            messages.error(request, 'This Email already taken..!')

    return render(request,'clientportal/addemail.html')


@login_required(login_url='login_client')
def addaddress(request):

    to_email = ''
    admin_user = User.objects.all().filter(is_superuser=True)[0]

    if request.method == 'POST':
        r  = Register.objects.filter(user_id=request.user.id)
        previous_address = r[0].address
        address = request.POST['address']
        r.update(address=address)
        # updated_address = r[0].address

        subject = "The User Address Update"

        body = "The Updated Details are: \n\n"\
            "Client ID: \t{}".format(r[0].client_id)+'\n'+\
            "User: \t\t{}".format(r[0].uname.upper())+'\n'+\
            "Previous Address: {}".format(previous_address)+'\n'+\
            "Updated Address: {}".format(address)

        from_email = 'support@hme158.com'
        if admin_user.email:
            to_email = admin_user.email
        else:
            to_email = from_email

        send_mail(
            subject,
            body,
            from_email,
            [to_email],
            fail_silently=False,
        )
        
        return redirect('profile')
    return render(request,'clientportal/profile.html')


def withdraw_divepay(request):

    if request.method == "POST":

        amount = request.POST.get('amount')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        w = UserWithdraw(amount = amount, username = username , email = email )
        w.save()
        return redirect(withdraw_divepay)
    return render(request,'clientportal/withdrawdivepay.html')


def testing_mail(request):
    send_to = "mbajaj2277@gmail.com"
    username = "mv3n0m"
    account_no = "111111"
    your_password = "123456789a"
    investor_pass = "1232431424"
    server_type = "Real"
    send_mail_func(send_to, username, account_no, your_password, investor_pass, server_type)
    return HttpResponse(send_to)


def send_mail_func(send_to=None, username=None, account_no=None, your_password=None, investor_pass=None, server_type=None,*args, **kwargs):
    data = {
        'user': username.title(),
        'login_account': account_no,
        'pwd': your_password,
        'inpwd': investor_pass,
        'server': server_type,
    }
    msg_text = """Dear {user},
    
congratulations，You just opened a new Real Account

Your account details， Please keep your information properly to avoid any loss：

Account Number：{login_account}
Password：{pwd}
Server：{server}
""".format(**data)
    from_mail = 'support@hme158.com'
    if send_to and your_password and account_no:
        send_mail("Your Account Details", msg_text, from_mail, [send_to], fail_silently=False)


def send_mail_func_demo(send_to=None, username=None, account_no=None, your_password=None, investor_pass=None, server_type=None,*args, **kwargs):
    print('-----------sendemail',send_to)
    data = {
        'user': username.title(),
        'login_account': account_no,
        'pwd': your_password,
        'inpwd': investor_pass,
        'server': server_type,
    }
    msg_text = """Dear {user},
congratulations，You just opened a new Demo Account
Your account details， Please keep your information properly to avoid any loss：
Account Number ： {login_account}
Password ： {pwd}
Server :  {server}
""".format(**data)

    from_mail = 'support@hme158.com'
    if send_to and your_password and account_no:
        send_mail("Your Account Details", msg_text, from_mail, [send_to], fail_silently=False)


def live_account_open_api_call(request_data):

    jwt_dict_data = {}
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'

    if request_data.POST.get('acctype') == 'Standard':
        jwt_dict_data = jwt_decode.dict_data
    elif request_data.POST.get('acctype') == 'Premium':
        jwt_dict_data = jwt_decode.dict_data_premium
    elif request_data.POST.get('acctype') == 'VIP':
        jwt_dict_data = jwt_decode.dict_data_vip
    else:
        jwt_dict_data = jwt_decode.dict_data_supreme

    jwt_dict_data['server'] = "Real"
    # jwt_dict_data['leverage'] = "1000"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.register.uname
    jwt_dict_data['client_email'] = request_data.user.register.email

    x_forwarded_for = request_data.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request_data.META.get('REMOTE_ADDR')

    jwt_dict_data['client_ip'] = client_ip
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}


from clientportal.models import LiveAcAmount, DemoAcAmount
@login_required(login_url='login_client')
# def laccount(request):

#     ac = []
#     response_data = {}
#     try:
#         if Register.objects.get(user=request.user.id).acc_type.all().exists():
#             ac=Register.objects.get(user=request.user.id).acc_type.all()
#         else:
#             ac=Addaccounttype.objects.all()
#     except:
#         pass

#     if request.method == "POST":
#         ac = request.POST.get('acctype')
#         ct = request.POST.get('ctype')
#         # if len(LiveAccount.objects.filter(user_id=request.user.id)) < 4:
#         if len(LiveAccount.objects.filter(user_id=request.user.id))+1 < int(Register.objects.get(user=request.user.id).acc_limit):
#             response_data = live_account_open_api_call(request)
#             r_data = response_data['data']
#             laccount_obj = LiveAccount(ac_type=ac, cu_type=ct, user_id=request.user.id, account_no=r_data.get('login'), balance=r_data.get('balance'), equity=r_data.get('equity'), group=r_data.get('group'))
#             laccount_obj.save()
#             lamount = LiveAcAmount(user=request.user, liveaccount=laccount_obj, amount=r_data['leverage'])
#             lamount.save()
#             print("New Live mt4 Created---|account number|-", r_data.get('login'), '|Password|-', r_data.get('password'), '|Investor Password|-', r_data.get('investor_pass'))
#             send_mail_func(
#                 send_to=r_data.get('email'),
#                 username=r_data.get('name'),
#                 account_no=r_data.get('login'),
#                 your_password=r_data.get('password'),
#                 investor_pass=r_data.get('investor_pass'),
#                 server_type=response_data['server'],
#             )
#             return redirect(live_account_response)
#         else:
            # messages.info(request, 'You have reached your limit, please contact Admin for further account access..!')
#     # else:
#     #     context_data = {'ac':ac, 'ca':Addcurrency.objects.all()}
#     return render(request,'clientportal/laccount.html', {'ac':ac, 'ca':Addcurrency.objects.all()})


def live_account_open_api_call1(request):
    url = 'https://live-six.divsolution.com/TradersDetails'
    response_api = requests.post(url)
    return {"data": response_api.text}

def common_helper_data():
    accessRights="FULL_ACCESS"
    brokerName='6i Group Limited'
    totalMarginCalculationType="MAX"
    leverageInCents=10
    groupName='A_XN_iVIP4_USD'
    return accessRights,brokerName,totalMarginCalculationType,leverageInCents,groupName
@login_required(login_url='login_client')
def laccount(request):
    reg=Register.objects.get(user=request.user)
    hashed_password = jwt_decode.hash_password(reg.pwd1)
    ref_id = 0
    ref_camp_code = ''
    ref_camp_name = ''
    register_id = request.user.register
    
    try:
        reg_ref_code = RegisterUserCampaign.objects.filter(register=register_id).first()
        ref_id = reg_ref_code.ref_code
        ref_camp_code = reg_ref_code.campaign_code
        ref_camp_name = reg_ref_code.campaign
    except Exception as e:
        print('----exception in uper---', e)
        pass
    ac = []
    response_data = {}
    try:
        if Register.objects.get(user=request.user.id).acc_type.all().exists():
            ac=Register.objects.get(user=request.user.id).acc_type.all()
        else:
            ac=Addaccounttype.objects.all()
    except:
        pass
    if request.method == "POST":
        ac = request.POST.get('acctype')
        ct = request.POST.get('ctype')
        accessRights,brokerName,totalMarginCalculationType,leverageInCents,groupName=common_helper_data()
        ct = request.POST.get('ctype')
        url = "https://live-six.divsolution.com/webserv/traders"
        payload = json.dumps({
        "accessRights": accessRights,
        "accountType": "HEDGED",
        "balance": 0,
        "brokerName":brokerName,
        "contactDetails": {
            "address": reg.address,
            "city": reg.city,
            "countryId": reg.country_id,
            "documentId": "0123",
            "email": reg.email,
            "phone": reg.mob,
            "state": reg.state,
            "zipCode": reg.pincode,
            "introducingBroker1": "CoolPartner",
            "introducingBroker2": "AnotherCoolPartner"
        },
        "depositCurrency": ct,
        "description": "coolDescription",
        "groupName": ac,
        "hashedPassword": hashed_password,
        "isLimitedRisk": False,
        "lastName": reg.lname,
        "leverageInCents": leverageInCents,
        "maxLeverage": 100000,
        "name": reg.fname+" "+reg.lname,
        "sendOwnStatement": True,
        "sendStatementToBroker": True,
        "totalMarginCalculationType": totalMarginCalculationType
        })
        headers = {
        'Content-Type': 'application/json'
        }

        if len(LiveAccount.objects.filter(user_id=request.user.id))+1 < int(Register.objects.get(user=request.user.id).acc_limit):

            response_api = requests.request("POST", url, headers=headers, data=payload)
            try:
                if response_api.status_code == 200:
                    r_data = json.loads(response_api.text)

                    # Access values by keys
                    
                    mt4_login = r_data["login"]
                  
                    laccount_obj = LiveAccount(ac_type=ac, cu_type=ct, user_id=request.user.id, account_no=r_data.get('login'), balance=r_data.get('balance'), 
                                               equity=r_data.get('equity'), group=r_data.get('groupName'),leverageInCents=r_data
                                               ['leverageInCents'],name=r_data['name'],lastName=r_data['lastName'],
                                               description=r_data['description'],accessRights=r_data['accessRights'],
                                               bonus=r_data['bonus'],nonWithdrawableBonus=r_data['nonWithdrawableBonus'],live_account_details=r_data)
                    laccount_obj.save()

                    lamount = LiveAcAmount(user=request.user, liveaccount=laccount_obj, amount=r_data['balance'])
                    lamount.save()

                    try:
                        reg_camp_insta = RegisterUserCampaign.objects.get(register=register_id, mt4_id=0, status=1)

                        if reg_camp_insta:
                            reg_camp_insta.mt4_id = mt4_login
                            reg_camp_insta.save()
                        else:
                            reg_obj = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=0, campaign_code='', campaign='', status=1)
                            reg_obj.save()

                    except Exception as e:
                        print('----exception in live account create-----', e)
                        reg_objs = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=0, campaign_code='', campaign='', status=1)
                        reg_objs.save()

                    print("New Live mt4 Created---|account number|-", r_data.get('login'), '|Password|-', r_data.get('password'), '|Investor Password|-', r_data.get('investor_pass'))

                    send_mail_func(
                        send_to=reg.email,
                        username=reg.uname,
                        account_no=r_data.get('login'),
                        your_password=reg.pwd1,
                        investor_pass=None,
                        server_type="Live",
                    )

                    return redirect(live_account_response)
            except:
                messages.info(request, 'New Live mt4 Account Not Created')
            
        else:
            messages.info(request, 'You have reached your limit, please contact Admin for further account access..!')
    return render(request,'clientportal/laccount.html', {'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()})

@login_required(login_url='login_client')
def user_live_details(request):
    obj=LiveAccount.objects.filter(user=request.user)
    dict_live_ac={
        "live_ac":obj
    }
    
    return render(request,'clientportal/index.html',dict_live_ac )


@login_required(login_url='login_client')
def demo_account_open_api_call(request_data):
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'
    jwt_dict_data = jwt_decode.dict_data_demo
    jwt_dict_data['server'] = "Demo"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.username
    jwt_dict_data['client_email'] = request_data.user.register.email
    jwt_dict_data['client_ip'] = request_data.META['REMOTE_ADDR']
    x_forwarded_for = request_data.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request_data.META.get('REMOTE_ADDR')

    jwt_dict_data['client_ip'] = client_ip
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}

@login_required(login_url='login_client')
def daccount(request):

    reg = Register.objects.get(user=request.user)
    response_data = {}
    if request.method == "POST":
        ac = request.POST['accounttype']
        ct = request.POST['ctype']
        hashed_password = jwt_decode.hash_password(reg.pwd1)
        import requests
        import json
        accessRights,brokerName,totalMarginCalculationType,leverageInCents,groupName=common_helper_data()
        url = "https://demo-six.divsolution.com/webserv/traders"

        payload = json.dumps({
            "accessRights":accessRights,
            "accountType": "HEDGED",
            "balance": 10000,
            "brokerName": brokerName,
            "contactDetails": {
                "address": reg.address,
                "city": reg.city,
                "countryId": int(reg.country_id),
                "documentId": "0123",
                "email": reg.email,
                "phone":reg.mob,
                "state":reg.state,
                "zipCode": reg.pincode,
                "introducingBroker1": "CoolPartner",
                "introducingBroker2": "AnotherCoolPartner"
            },
            "depositCurrency":ct,
            "description": "coolDescription",
            "groupName": ac,
            "hashedPassword": hashed_password,
            "isLimitedRisk": False,
            "lastName": reg.lname,
            "leverageInCents": leverageInCents,
            "maxLeverage": 100000,
            "name": reg.fname+" "+reg.lname,
            "sendOwnStatement": True,
            "sendStatementToBroker": True,
            "totalMarginCalculationType": "MAX"
            })
        headers = {
        'Content-Type': 'application/json'
        }
        
        if len(DemoAccount.objects.filter(user_id=request.user.id))+1 < int(Register.objects.get(user=request.user.id).demo_acc_limit):
            
            # Access values by keys
            try:
                response_api = requests.request("POST", url, headers=headers, data=payload)
                print("=====response_data===",response_api.status_code,response_api.text)
                r_data = json.loads(response_api.text)
                if response_api.status_code == 200:
                    mt4_login = r_data["login"]
                    daccount_obj = DemoAccount(ac_type=ac, cu_type=ct, user_id=request.user.id, account_no=r_data.get('login'),
                                                balance=r_data.get('balance'), equity=r_data.get('equity'), group=r_data.get('group'))
                    daccount_obj.save()
                    damount = DemoAcAmount(user=request.user, demoaccount=daccount_obj, amount=r_data['balance'])
                    damount.save()

                    print("New Demo mt4 Created---|acount number|-",r_data.get('login'), '|Password|-', r_data.get('password'), '|Investor Password|-', r_data.get('investor_pass'))
                   
                    # send_mail_func_demo(
                        # send_to=reg.email,
                        # username=reg.uname,
                        # account_no=r_data.get('login'),
                        # your_password=reg.pwd1,
                        # investor_pass=None,
                        # server_type="Demo",
                    # )
                    return redirect(demo_account_response)
            except:
                messages.info(request, "Demo Account Not Created")
        else:
            messages.info(request, 'You have reached your limit, please contact Admin for further account access..!')
    else:
        context_data ={'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()}
    return render(request,'clientportal/daccount.html', {'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()})


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
        return decode_jwt(
            data=response_api.text)

    def get(self, request, *args, **kwargs):

        data = self.account_detail_url(self.request)
        if data['status'] == 0:
            return data['msg']
        return HttpResponse("Demo account detail")



def call_edit(request):

    data = {
        "account":'8000048',
        "campaignCode":'ITj[2q0^',
        "ibId":'10001'
    }

    edit_mt4_account_api_call(data)
    return JsonResponse({'message':'done'})


def set_language(request, language):

    old_lang = translation.get_language()
    translation.activate(language)
    return redirect('/clientportal', lang=language)


def make_password(stringLength=15):

    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))


@login_required(login_url='login_client')
def dashboard(request):

    live_acounts = LiveAccount.objects.filter(user=request.user)
    demo_acounts = DemoAccount.objects.filter(user=request.user)
    return render(request,'clientportal/client_index.html', {'lives':live_acounts, 'demos':demo_acounts})
    # return render(request,'clientportal/client_index.html')


def settings(request):
    return render(request,'clientportal/settings.html')


def performance(request):
    return render(request,'clientportal/performance.html')


def deposit_divepay(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositdivepay.html',{'ca':ca})


def deposit_neteller(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositneteller.html',{'ca':ca})


def deposit_skrill(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositskrill.html',{'ca':ca})
def wallet_to_live_transfer(request,transfer_from,transfer_from_to,amount):
    reg=Register.objects.get(user=request.user)
    print("==Register=======",reg)
    usr_wal=UserWallet.objects.get(user=request.user)
    login=transfer_from_to
    client_ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('HTTP_X_REAL_IP', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('REMOTE_ADDR', None)
    print("=====client_ip_address==",client_ip_address)
    url = "https://live-six.divsolution.com/deposite"

    payload = json.dumps({
    "login": login,
    "preciseAmount":amount
    })
    headers = {
        'Content-Type': 'application/json'
    }
    if float(usr_wal.amount)>=float(amount):
        response = requests.request("POST", url, headers=headers, data=payload)

        print("=======",response.text)
        wal_obj=WalletFinance.objects.create(
            user=request.user ,client_id=reg.client_id,name=reg.fname+" "+reg.lname,
            amount=amount,t_ip=client_ip_address,currency="USD"
            
        )
        UserDeposits.objects.create(walletfinance=wal_obj)
        
        usr_wal.amount=float(usr_wal.amount)-float(amount)
        usr_wal.save()
        return 0
    else:
        return 1

def live_to_live_transfer(request, transfer_from, transfer_from_to, amount):
    import json
    import requests
   

    reg = Register.objects.get(user=request.user)
    print("==Register=======", reg)
    login = transfer_from_to
    client_ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('HTTP_X_REAL_IP', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('REMOTE_ADDR', None)
    url = "https://live-six.divsolution.com/TradersDetails"

    payload = json.dumps({
        "login": transfer_from
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    json_response = json.loads(response.text)
    print("==================", json_response['balance'])
    deposit_url = "https://live-six.divsolution.com/deposite"
    withdraw_url = "https://live-six.divsolution.com/withdraw"
    deposit_payload = json.dumps({
        "login": login,
        "preciseAmount": amount
    })
    withdraw_payload = json.dumps({
        "login": transfer_from,
        "preciseAmount": amount
    })
    headers = {
        'Content-Type': 'application/json'
    }
    if float(json_response['balance'])/100 >= float(amount):
        deposit_response = requests.request("POST", deposit_url, headers=headers, data=deposit_payload)

        print("=======", deposit_response.text)
        withdraw_response = requests.request("POST", withdraw_url, headers=headers, data=withdraw_payload)

        print("=======", withdraw_response.text)
        wal_obj = WalletFinance.objects.create(
            user=request.user, client_id=reg.client_id, name=reg.fname + " " + reg.lname,
            amount=amount, t_ip=client_ip_address,currency="USD"
            
        )
        # UserDeposits.objects.create(walletfinance=wal_obj)
        # usr_wal=UserWallet.objects.get(user=request.user)
        # usr_wal.amount=float(usr_wal.amount)-float(amount)
        # usr_wal.save()
        return 0
    else:
        return 1


def live_to_wallet_transfer(request, transfer_from, transfer_from_to, amount):
    import json
    import requests
    reg = Register.objects.get(user=request.user)
    print("==Register=======", reg,transfer_from)
    login = transfer_from_to
    client_ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('HTTP_X_REAL_IP', None)

    if client_ip_address is None:
        client_ip_address = request.META.get('REMOTE_ADDR', None)
    print("=====client_ip_address==",client_ip_address)
    url = "https://live-six.divsolution.com/TradersDetails"

    payload = json.dumps({
        "login": transfer_from
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    json_response = json.loads(response.text)
    print("==================", json_response['balance'])
    # deposit_url = "https://ditscrm.divsolution.com/deposite"
    withdraw_url = "https://live-six.divsolution.com/withdraw"
    # deposit_payload = json.dumps({
    #     "login": login,
    #     "preciseAmount": amount
    # })
    withdraw_payload = json.dumps({
        "login": transfer_from,
        "preciseAmount": amount
    })
    headers = {
        'Content-Type': 'application/json'
    }
    if float(json_response['balance'])/100 >= float(amount):
        # deposit_response = requests.request("POST", deposit_url, headers=headers, data=deposit_payload)

        # print("=======", deposit_response.text)
        withdraw_response = requests.request("POST", withdraw_url, headers=headers, data=withdraw_payload)

        print("=======", withdraw_response.text)
        wal_obj = WalletFinance.objects.create(
            user=request.user, client_id=reg.client_id, name=reg.fname + " " + reg.lname,
            amount=amount, t_ip=client_ip_address,currency="USD"
            
        )
        # UserDeposits.objects.create(walletfinance=wal_obj)
        usr_wal=UserWallet.objects.get(user=request.user)
        usr_wal.amount=float(usr_wal.amount)+float(amount)
        usr_wal.save()
        return 0
    else:
        return 1

@login_required(login_url='login_client')
def manage_funds(request):
    
    if request.method == "POST":
        
        transfer_from = request.POST.get('transfer_from')
        transfer_from_to = request.POST.get('transfer_from_to')
        amount = request.POST.get('amount')
        if transfer_from == 'wal_0' and transfer_from_to!= 'wal_0':
            val=wallet_to_live_transfer(request,transfer_from,transfer_from_to,amount)
            return JsonResponse({"data":val})
        if transfer_from != 'wal_0' and transfer_from_to!= 'wal_0':
            val=live_to_live_transfer(request,transfer_from,transfer_from_to,amount)
            return JsonResponse({"data":val})
        else:
            if transfer_from != 'wal_0' and transfer_from_to== 'wal_0':
                val=live_to_wallet_transfer(request,transfer_from,transfer_from_to,amount)
                return JsonResponse({"data":val})
    else:
        live_acounts = LiveAccount.objects.filter(user=request.user)
        return render(request,'clientportal/managefunds.html',{'lives':live_acounts})
def account_details(request):
    live_acounts = LiveAccount.objects.filter(user=request.user)
    url = "https://live-six.divsolution.com/TradersDetails"

    
    for liv in live_acounts:
        payload = json.dumps({
        "login": liv.account_no
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        json_response = json.loads(response.text)
        print("==================", json_response['balance'])
        liv.balance=float(json_response['balance'])/100
        liv.save()
    return JsonResponse({"data":0})
    

def depositfailure(request):
    return render(request, 'clientportal/depositfailure.html')


@login_required(login_url='login_client')
def bitcoin_payment(request):
    return render(request, 'clientportal/bitcoinpayment.html')


@login_required(login_url='login_client')
def bitcoin_withdraw(request):
    return render(request, 'clientportal/bitcoin_withdraw.html')


@login_required(login_url='login_client')
def usdt(request):
    return render(request, 'clientportal/bitcoinpayment.html')

@login_required(login_url='login_client')
def usdt_withdraw(request):
    return render(request, 'clientportal/usdt_withdraw.html')


def depositsuccess(request):
    return render(request, 'clientportal/usdt.html')

@login_required(login_url='login_client')
def deposit(request):
    
        
    return render(request,'clientportal/deposit.html')

@login_required(login_url='login_client')
def withdraw(request):
    
    return render(request,'clientportal/withdraw.html')

@login_required(login_url='login_client')
def live_account_reset_password(request):
    if request.method == "GET":
        # login = request.POST.get('login')
        # amount = request.POST.get('preciseAmount')
        login=1007252
        hashedPassword="19a9f9cc428ba55dd25c59bc84ba27cb"
        url = "https://live-six.divsolution.com/changepassword"

        payload = json.dumps({
        "login": login,
        "hashedPassword":hashedPassword
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    return JsonResponse({"data":"success"})

def live_account_response(request):
    return render(request,'clientportal/live_account_response.html')


def demo_account_response(request):
    return render(request,'clientportal/demo_account_response.html')


    # chait_
# def forgot_password(request):

#     if request.method == 'POST':
#         email = request.POST['email']
#         try:
#             user = User.objects.get(email=email)
#         except:
#             user = False
#         if user:
#             request.session['user_name'] = user.user_name
#             otp = randint(1000, 99999)
#             request.session['otp'] = otp
#             request.session.set_expiry(120)
#             subject = 'OTP Requested for forgotten password'
#             message = "We received a forgot password request from your account.\nMake sure not to share your OTP with anyone.\n OTP :{}.\n\n\nplease verify your account if it's not you".format(
#                 str(otp))
#             from_email = settings.EMAIL_HOST_USER
#             # send_mail(subject, message, from_email,
#             #           [email], fail_silently=False)
#             return redirect('otp')
#         else:
#             messages.error(request, 'Enter a valid Registered Email or ')
#             messages.error(request, 'Your profile data is Incomlete ')
#             return redirect('forgot_password')
#     return render(request, 'clientportal/forget_password_confirm.html', {})


# def otp(request):

#     if request.method == 'POST':
#         otp = request.POST['otp']

#         if int(request.session['otp']) == int(otp):
#             return redirect('reset_password')
#         else:
#             messages.error(request, 'Your otp expired or')
#             messages.error(request, 'invalid OTP, try again')
#             return redirect('otp')

#     return render(request, 'otp.html', {})


# def reset_password(request):

#     rocks12 = User.objects.get(user_name=request.session['user_name'])
#     if request.method == 'POST':
#         email = rocks12.email
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
        
#         if password == confirm_password:
#             rocks12.password = make_password(password)
#             rocks12.save()
#             subject = request.session['user_name'].capitalize(
#             ) + "Your Password reset"
#             message = 'Please find your account details below with credentials after password reset \nEmail :{}\nUser Name :{}\nPassword :{}'.format(
#                 email.lower(), request.session['user_name'], str(password))
#             from_email = settings.EMAIL_HOST_USER
            # send_mail(
            #     subject,
            #     message,
            #     from_email,
            #     [email],
            #     fail_silently=False,
            # )
#             return redirect('login')
#         else:
#             messages.error(request, 'password mis match')
#             return redirect('reset_password')
#     return render(request, 'clientportal/forget_password_confirm.html', {})

# chait_

def client_trade_history(request):
    return render(request,'clientportal/client_trade_history.html')
from datetime import datetime, time, timedelta
def positions_api_call(request,client_id,mt5_login,min_date,max_date):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    email=User.objects.get(username=request.user).email
    # current_time = datetime.now().time()

    # # Convert date string to datetime object
    # date_obj = datetime.strptime(min_date, "%Y-%m-%d").date()

    # # Create datetime object with concatenated date and current time
    # combined_datetime = datetime.combine(date_obj, current_time)

    # print(f"Combined DateTime: {combined_datetime}")
    url = "https://demo-hme.divsolution.com/closedPositions"

    payload = json.dumps({
      "fromDate": "2024-03-27T12:12:12.000",
      "toDate": "2024-03-29T12:12:12.000",
      "Login": "8000055"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


    
    val=json.loads(response.text)
    
    
    
    if len(val)>0:
        for i in range(len(val)):
            
            
            login_account=val[i]['login']
            
            print(val[i]['positionId'])
            symbol=val[i]['symbol']
            positionId=val[i]['positionId']
            direction=val[i]['direction']
            volume=val[i]['volume']
            openTimestamp=val[i]['openTimestamp']
            closeTimestamp=val[i]['closeTimestamp']
            closePrice=val[i]['closePrice']
            commission=val[i]['commission']
            swap=val[i]['swap']
            entryPrice=val[i]['entryPrice']
            dealId=val[i]['dealId']
            trade_type="closedPositions"
            if login_account:
                api=Positions(client_id=client_id,login_account=login_account,symbol=symbol,positionId=positionId,
                                direction=direction,bookType=val[i]['bookType'],trade_type=trade_type,
                              volume=volume,openTimestamp=openTimestamp,closeTimestamp=closeTimestamp,
                              closePrice=closePrice,commission=commission,entryPrice=entryPrice,dealId=dealId)
                api.save()
        status=0
        return status
    else:
        status=1
        return status
        

@login_required(login_url='login_client')
def client_trade_position(request):
    email=User.objects.get(username=request.user).email
    client_id=Register.objects.get(email=email).client_id
    if request.method == 'POST':
        mt5_login=request.POST.get('mt5_login')
        
        min_date=request.POST.get('min')
        max_date=request.POST.get('max')
        status=positions_api_call(request,client_id,mt5_login,min_date,max_date)
        return JsonResponse({'data':status})
    else:
        user=Register.objects.get(uname=request.user).client_id
        print("=======Login_account==========",LiveAccount.objects.filter(user=request.user))
        e=Positions.objects.filter(client_id=user)
        val=[]
        for t in e:
               
            d = t.added_on.strftime("%m/%d/%Y, %H:%M:%S")
            dt, tm = d.split(', ')
            mnt, dy, yr = dt.split('/')
            hrs,mt,sc = tm.split(':')
            dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
            val.append((dttm,t))
        val=[r for r in sorted(val,key=lambda x:x[0],reverse=True)]
        context_data={
            'mt5_login':LiveAccount.objects.filter(user=request.user),
            'positions':val
        }
    return render(request,'clientportal/client_trade_position.html',context_data)