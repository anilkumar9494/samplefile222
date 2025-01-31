import unicodecsv as csv
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render,redirect,HttpResponse
# from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Securityque
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth.models import User
from .models import Addsalesnotes, SalesQueue, SalesAssignment
from .models import Agentusercreate,Comments,Transaction_Method,transaction_ibmethod_mdl
from .models import Adddepartment,Addoffice,Addbrand,Access_level,Leads_access_level,Addleadsregions
from .models import Addaccounttype,Adddepartment
from .models import Access_level,Leads_access_level
from common.models import Country
from .models import Addcurrency,Addbrand,Addleadsregions,Adddepartment,Addoffice
from clientportal.models import Uploaddocument, UserWithdraw
from django.contrib.auth.models import User
from django.contrib import auth
# import django_filters
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from clientportal.models import UserDeposits,UserWithdraw, WalletFinance,UserWallet
import requests
# from urllib import request
import jwt
from clientportal.models import UserDeposits, UserWithdraw ,LiveAccount
import json
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from sportapp.models import Register
from .filters import DateRangeMaker, UserDepositsDjangoFilter, UserDepositsDjangoFilterCustomDate
from datetime import datetime as dt
from clientportal.models import UserDeposits, UserWithdraw
from django.db import IntegrityError
from django.db.models import Sum
from datetime import datetime
import io
import os
import xlwt
from urllib.parse import urlparse
from rest_framework.generics import RetrieveAPIView
from django.contrib import messages
from .forms import RegisterUpdateForm


class ToPDF:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = landscape(A4)
        elif pagesize == 'letter':
            self.pagesize = landscape(letter)
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

        self.width, self.height = self.pagesize

    def output(self, data_list, title_headers, flag=None):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=20,
                                leftMargin=20,
                                topMargin=40,
                                bottomMargin=40,
                                pagesize=self.pagesize)

        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CenterAlign', fontName='Vera', alignment=TA_CENTER))
        if flag == 'finance':
            colWidths = [120, 160, 80, 80, 80]
        elif flag == 'trans_history':
            colWidths = [120, 60, 80, 130, 80, 80, 80]
        else:
            elements.append(Paragraph('Transactions\n', styles['CenterAlign']))
            colWidths = [120, 50, 50, 120, 60, 90, 60, 60]
        table_data = []
        table_data.append(title_headers)
        table_data.extend(data_list)
        trans_table = Table(table_data, colWidths=colWidths)
        trans_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Vera'),
                                        ('ALIGN',(0, 0),(-1,-1),'CENTER'),
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                        ('INNERGRID', (0, 0), (-1, 1), 0.25, colors.white),
                                        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(trans_table)
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

class Echo:
    def write(self, value):
        return value


@login_required(login_url='admin_login')
def home(request):

    type_1_amount=''
    type_2_amount=''
    today = datetime.today()
    today_register = Register.objects.filter(added_on__contains=today.date())
    try:
        type_1_amount = Transaction_Method.objects.filter(type = 1, added_on__month=today.month).aggregate(Sum('amount'))['amount__sum']
    # amt_1 = type_1_amount
        type_2_amount = Transaction_Method.objects.filter(type = 2, added_on__month=today.month).aggregate(Sum('amount'))['amount__sum']
    # amt_2 = type_2_amount
    except:
        pass
    context = {
        'total_clients': Register.objects.all().count(),
        'today_register': today_register.count(),
        'this_month_deposit': round(type_1_amount, 2) if type_1_amount else 0,
        'this_month_withdraw': round(type_2_amount, 2) if type_2_amount else 0,
    }
    return render(request,'dashboard/temp/crm_home.html', context)


def admin_login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect(home)
            else:
                return render(request,'dashboard/temp/login.html',{'error':'You are not authenticated as admin'})
        else:
            return render(request,'dashboard/temp/login.html',{'error':'Invalid Login Credentials'})
    else:
        context_data={
        'u':User.objects.all()
        }
        return render(request,'dashboard/temp/login.html',context_data)


def admin_logout(request):

    auth.logout(request)
    return redirect(admin_login)


@login_required(login_url='admin_login')
def client(request):

    reg_users = Register.objects.all()
#    url = f'https://hme158.com/api/v1/auth/get_register_user_campaign'
    url = f'https://www.hme158.com/api/v1/auth/get_register_user_campaign'
    json_data = requests.get(url).json()

    for data in json_data:
        for users in reg_users:
            if users.id == data['register'] and data['status'] != 0 and data['ref_code'] != 0 and data['ref_code'] != '':
                reg_obj = Register.objects.get(id=users.id)
                reg_obj.sans = data['ref_code']
                reg_obj.save()

    url_2 = f'https://ib-portal.hme158.com/api/v1/ib_users'
    data_json = requests.get(url_2).json()
    for json in data_json:
        for users in reg_users:
            if users.client_id == json['client_id']:
                reg_obj_id = Register.objects.get(id=users.id)
                reg_obj_id.client_ib = json['ib_id']
                reg_obj_id.save()

                # print('--------users client_id---------', json['client_id'])
                # print('--------users client_id---------', reg_obj_id.client_ib)

    return render(request,'dashboard/temp/crm_client_detail.html', {'reg_users': reg_users})


from sport import settings
@login_required(login_url='admin_login')
def client_update(request, pk):
    print('okkk000000000000000000000000000000000000000000000000000000000000000')
    # to_email_2 = ''
    reg_data = Register.objects.get(user_id=pk)
    print('reg_data-----------',reg_data)
    user_data = User.objects.get(id=pk)

    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        form = RegisterUpdateForm(request.POST, instance=reg_data)

        if form.is_valid():
            if int(request.POST.get('acc_limit')) >= 4 and int(request.POST.get('demo_acc_limit')) >= 2:
                user_data.username = username
                user_data.email = email
                form.save()
                user_data.save()
                subject = "User Updated profile data..."

                body = "更新的细节是: \n\n"\
                    "客户 ID : {} ".format(reg_data.client_id)+'\n'+\
                    "过去登录用户名: {} ".format(reg_data.uname)+'\n'+\
                    "当前登录用户名: {} ".format(username)+'\n'+\
                    "更新的电子邮件 : {} ".format(email)+'\n'+\
                    "更新日期 : {} ".format(dob)+'\n'+\
                    "更新地址 : {} ".format(address)

                from_email = settings.EMAIL_HOST_USER

                if reg_data.email:
                    to_email = reg_data.email
                else:
                    to_email = request.POST.get("email")

                send_mail(subject,body,from_email,[to_email],fail_silently=False,)

                return redirect('client')
            else:
                messages.error(request, 'Can not Decrease the Account Limit as provided default..!')                
        # else:
        #     messages.error(request, 'Email already taken Please provide another...!')
    else:
        form = RegisterUpdateForm(instance=reg_data)
        # messages.error(request, 'Email already taken Please provide another...!')
    return render(request, 'dashboard/temp/client_edit.html', {'form': form, 'reg_data':reg_data,})


@login_required(login_url='admin_login')
def client_delete(request, pk):
    try:
        reg_obj = Register.objects.get(user_id=pk)
        reg_user_camp = RegisterUserCampaign.objects.get(register__id=pk)
        user_obj = User.objects.get(id=pk)
        reg_obj.delete()
        user_obj.delete()
        reg_user_camp.delete()
    except:
        messages.error(request, 'Objects deleted already..!')
    return redirect('client')


def pendingclients(request):

    year_val = ''
    month_val = ''
    date_val = ''
    un_verified_users = Register.objects.filter(verify=False)

    for users in un_verified_users:
        date_split = str(users.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
    
    return render(request,'dashboard/temp/crm_pending_client.html', {
                                'un_verified_users':un_verified_users,
                                'added_on_year_val': year_val,
                                'added_on_month_val': month_val,
                                'added_on_date_val': date_val,
                                }
                            )


def resend_email(request):

    client_id = request.GET.get('client_id')
    user = get_object_or_404(Register.objects.filter(client_id=client_id))
    link = request.build_absolute_uri(reverse('verify_mail',kwargs={'client_id':client_id}))
    subject = 'Please Verify your email'
    message = link
    to_email = str(user.email)
    from_mail = settings.EMAIL_HOST_USER
    send_mail(subject,message,from_mail,[to_email])
    return redirect(pendingclients)


def verify_mail(request,client_id):

    client_id=client_id
    Register.objects.filter(client_id=client_id).update(verify=True)
    return render(request,'login.html',{})


def search_by_id(request):

    r = None
    if request.method == 'GET':
        user_id = request.GET.get('by_id')
        try:
            r = Register.objects.filter(client_id__icontains=user_id)
        except:
            pass
    return render(request,'dashboard/temp/client.html',{'r':r})


def search_by_name(request):

    r = None
    if request.method == 'GET':
        name = request.GET.get('name')
        try:
            r = Register.objects.filter(fname__icontains=name)
        except:
            pass
    return render(request,'dashboard/temp/client.html',{'r':r})


def search_by_email(request):

    r = None
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            r = Register.objects.filter(email__icontains=email)
        except:
            pass
    return render(request,'dashboard/temp/client.html',{'r':r})


def search_by_mt4(request):

    r=None
    if request.method == 'GET':
        mt4 = request.GET.get('mt4')
        try:
            mt4_user = LiveAccount.objects.filter(account_no=mt4)
            for x in mt4_user:
                register_user_id = x.user.pk
                r = Register.objects.filter(user=register_user_id)
        except:
            pass
    return render(request,'dashboard/temp/client.html',{'r':r,'mt4_user':mt4_user})


@login_required(login_url='admin_login')
def clientnotes(request):
    return render(request,'dashboard/temp/clientnotes.html')


@login_required(login_url='admin_login')
def client_all_information(request, client_id):

    reg_data = Register.objects.get(id=client_id)
    docs = Uploaddocument.objects.get(user_id=request.GET.get('u_id'))
    
    return render(request,'dashboard/temp/client_detail_index.html', {'reg_data':reg_data, 'docs':docs})


from clientportal.models import LiveAcAmount, DemoAcAmount

@login_required(login_url='admin_login')
def liveaccount(request):

    docs = []
    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)

    try:
        docs = Uploaddocument.objects.get(user_id=request.GET.get('u_id'))
        user_wallet = UserWallet.objects.get(user_id=user_id)
    except:
        docs = ''
        user_wallet = ''
        # pass
    # endpoint = f"{settings.HME_CLIENT}/api/v1/live_accounts/{user_id}"
    # req = requests.get(endpoint)
    # req_json = req.json()
    lamount = LiveAcAmount.objects.filter(user_id=user_id)

    return render(request,'dashboard/temp/crm_live_account.html', {'reg_data':reg_data, 'docs':docs, 'lacs':lamount, 'wallet':user_wallet})


@login_required(login_url='admin_login')
def demoaccount(request):

    docs = []
    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)

    try:
        docs = Uploaddocument.objects.get(user_id=request.GET.get('u_id'))
        user_wallet = UserWallet.objects.get(user_id=user_id)
    except:
        docs = ''
        user_wallet = ''
        # pass

    damount = DemoAcAmount.objects.filter(user_id=user_id)

    return render(request,'dashboard/temp/crm_demo_account.html', {'reg_data':reg_data, 'docs':docs, 'dacs':damount, 'wallet':user_wallet})


@login_required(login_url='admin_login')
def finance(request, exporttype=None):

    docs = []
    user_id = request.GET.get('u_id')

    try:
        docs = Uploaddocument.objects.get(user_id=request.GET.get('u_id'))
        user_wallet = UserWallet.objects.get(user_id=user_id)
    except:
        user_wallet = ''
        docs = ''
        # pass

    reg_data = Register.objects.get(user_id=user_id)
    wallet = WalletFinance.objects.filter(user_id = int(request.GET.get('u_id'))).order_by('-id')
    transaction = Transaction_Method.objects.filter(user=int(request.GET.get('u_id'))).order_by('-id')

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

    for i in transaction:
        date_split = str(i.added_on).split(' ')[0]
        time_split = str(i.added_on).split(' ')[1]
        hour_val = time_split.split(':')[0]
        minute_val = time_split.split(':')[1]
        sec_val = time_split.split(':')[2]
        split_data = sec_val.split('.')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        id = i.id
        t = i.type
        amount = i.amount
        currency = i.currency.name
        comments = i.comments.name
        if comments == "Virtual currency":
            currency_type = "Crypto"
        else:
            currency_type = "USDT"
        if t == '1':
            transfer_type = "Deposit from"
        else:
            transfer_type = "Withdraw from"
        response_list.append((year_val+month_val+date_val, {
            'added_on_year_val': year_val,
            'added_on_month_val': month_val,
            'added_on_date_val': date_val,
            'added_on_hour_val': hour_val,
            'added_on_minute_val': minute_val,
            'added_on_sec_val': split_data,
            'id':id,
            'transfer_type':transfer_type,
            'currency':"USD",
            'comments':comments,
            'amount':amount,
            'added_on':i.added_on,
            'get_status_display':"Completed"
        }))

    for i in wallet:
        date_split = str(i.added_on).split(' ')[0]
        time_split = str(i.added_on).split(' ')[1]
        hour_val = time_split.split(':')[0]
        minute_val = time_split.split(':')[1]
        sec_val = time_split.split(':')[2]
        split_data = sec_val.split('.')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        if i.type == 1:
            transfer_type = 'Transfer From'
            type = 'Transfer IN'
        elif i.type == 2:
            transfer_type = 'Transfer To'
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
            currency = 'USD'

        response_list.append((year_val+month_val+date_val, {
                'amount':i.amount,
                'type':type,
                'added_on':i.added_on,
                'currency':currency,
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'added_on_hour_val': hour_val,
                'added_on_minute_val': minute_val,
                'added_on_sec_val': split_data,                
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
        }))
    response_data = [d[1] for d in sorted(response_list, key=lambda x:x[0])]
    if exporttype:
        response_list = []
        title_headers = ["Date", "Content", "Amount", "Currency", "Status"]
        for rd in response_data:
            dt = f"{rd['added_on_year_val']}-{rd['added_on_month_val']}-{rd['added_on_date_val']} {rd['added_on_hour_val']}:{rd['added_on_minute_val']}:{rd['added_on_sec_val']}"
            if rd.get('type'):
                details = f"{rd['transfer_type']} {rd['transfer_to']}"
            else:
                details = f"{rd['transfer_type']} {rd['comments']}"
            amt = rd['amount']
            curr = rd['currency']
            status = rd['get_status_display']
            response_list.append([dt, details, amt, curr, status])
        return exportData(response_list, exporttype, 'finance', title_headers)
    else:
        # user_id = request.GET.get('u_id')
        # reg_data = Register.objects.filter(user_id=user_id)        
        return render(request, 'dashboard/temp/crm_finance.html',{'response_list':response_data, 'reg_data':reg_data, 'docs':docs, 'wallet':user_wallet})


def exportData(data_list, exporttype, table_name, title_headers):

    if exporttype == 'pdf':

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Report_{}.pdf'.format(dt.now())
        buffer = io.BytesIO()
        report = ToPDF(buffer, 'A4')
        pdf = report.output(data_list, title_headers, table_name)
        response.write(pdf)
        return response

    if exporttype == 'excel':

        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename=Report_{dt.now()}.xls"
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Summary")
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for i in range(len(title_headers)):
            worksheet.write(0, i, title_headers[i], font_style)
        for idx, hist in enumerate(data_list):
            for i, val in enumerate(hist):
                worksheet.write(idx+1, i, val)
        
        # for idx, hist in enumerate(data_list):
        #     for val in hist.values():
        #         total_trans += float(val['amount'])
        #         for i, v in enumerate(val.values()):
        #             worksheet.write(idx+1, i, v)
        #
        # if t == '1':
        #     worksheet.write(total_N+2, 5, "Total Deposits", font_style)
        #     worksheet.write(total_N+2, 6, total_trans, font_style)
        # elif t == '2':
        #     worksheet.write(total_N+2, 5, "Total Withdrawal", font_style)
        #     worksheet.write(total_N+2, 6, total_trans, font_style)
        workbook.save(response)
        return response

    if exporttype == 'csv':

        rows = [title_headers,]
        for hist in data_list:
            rows.append(hist)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer, encoding='utf-8')
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        # response['Transfer-Encoding'] = 'chunked'
        # response.charset = 'UTF-8'
        response['Content-Disposition'] = f'attachment; filename="Report_{dt.now()}.csv"'
        return response


@login_required(login_url='admin_login')
def agents(request):

    agents = Agentusercreate.objects.all()
    return render(request,'dashboard/temp/crm_agent.html',{'agents':agents})


@login_required(login_url='admin_login')
def adduser(request):
    return render(request,'dashboard/temp/crm_adduser.html')

@login_required(login_url='admin_login')
def documents(request):

    docs = []
    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)

    try:
        docs = Uploaddocument.objects.filter(user_id = user_id).first()
        user_wallet = UserWallet.objects.get(user_id=user_id)
    except:
        user_wallet = ''
        docs = ''
        # pass

    return render(request,'dashboard/temp/documents.html', {'docs':docs, 'reg_data':reg_data, 'u_id':user_id, 'wallet':user_wallet})


@login_required(login_url='admin_login')
def verify_document(request):

    if request.GET.get('u_id'):
        ui_d = request.GET.get('u_id')
    else:
        ui_d = ''

    reg_data = Register.objects.get(user_id= request.GET.get('u_id'))
    docs = Uploaddocument.objects.filter(user_id = request.GET.get('u_id')).first()

    if docs.status == 2:
        Uploaddocument.objects.filter(user=request.GET.get('u_id')).update(type=2, approve=True)
        docs = Uploaddocument.objects.filter(user_id = request.GET.get('u_id')).first()
    else:
        messages="Documents were not uploaded by the client...!"
        return redirect('client')

    return render(request,'dashboard/temp/documents.html', {'docs':docs, 'reg_data':reg_data, 'u_id':ui_d})


def unverify_documents(request):

    if request.GET.get('u_id'):
        ui_d = request.GET.get('u_id')
    else:
        ui_d = ''

    reg_data = Register.objects.get(user_id=request.GET.get('u_id'))
    docs = Uploaddocument.objects.filter(user_id = request.GET.get('u_id')).first()

    if docs.status == 2:
        Uploaddocument.objects.filter(user=request.GET.get('u_id')).update(type=1, approve=False)
        docs = Uploaddocument.objects.filter(user_id = request.GET.get('u_id')).first()
    else:
        messages="Documents were not uploaded by the client...!"
        return redirect('client')

    return render(request,'dashboard/temp/documents.html', {'docs':docs, 'reg_data':reg_data, 'u_id':ui_d})


@login_required(login_url='admin_login')
def pendingpartner(request):
    return render(request,'dashboard/temp/pendingpartner.html')


@login_required(login_url='admin_login')
def pendingleverage(request):
    return render(request,'dashboard/temp/pendingleverage.html')


@login_required(login_url='admin_login')
def clientview(request,clientid):
    r = Register.objects.get(id=clientid)
    return render(request,'dashboard/temp/clientview.html',{'r':r})


@login_required(login_url='admin_login')
def addsalesnotes(request):

    docs = []
    context_data = {}
    user_id=request.GET.get('u_id')

    reg_data = Register.objects.get(user_id=request.GET.get('u_id'))

    try:
        docs = Uploaddocument.objects.get(user_id=user_id)
    except:
        pass
    
    if request.method == 'POST':
        note = request.POST['note']
        client_id = request.POST['cid']
        u_id = request.POST['uid']
        salesnote = Addsalesnotes.objects.create(created_by=request.user, user=reg_data, note=note, client_id=client_id)
        return redirect('/dashboard/sale-notes?u_id='+str(u_id))
    else:
        context_data = {
            'notes':Addsalesnotes.objects.filter(user=reg_data).order_by('-id'),
            'uid':user_id,
            'reg_data':reg_data,
            'docs':docs,
        }

    return render(request,'dashboard/temp/sales_note.html', context_data)


@login_required(login_url='admin_login')
def update_sales_notes(request, sales_id):
    
    docs = []
    user_id = request.GET.get('u_id')
    note_obj = Addsalesnotes.objects.get(id=sales_id)
    reg_data = Register.objects.get(id=note_obj.user_id)

    try:
        docs = Uploaddocument.objects.get(user_id=note_obj.user_id)
    except:
        pass

    if request.method == 'POST':
        notes = request.POST['notes']
        u_id = request.POST['uid']
        request.session['u_id'] = u_id
        note_obj.note = notes
        note_obj.user_id = note_obj.user_id
        note_obj.save()

        messages.success(request, 'Note updated successfully...!')
        return redirect('/dashboard/sale-notes?u_id='+str(u_id))

    return render(request,'dashboard/temp/sales_note_edit.html', {'notes':note_obj, 'uid':user_id, 'docs':docs,'reg_data':reg_data,})


@login_required(login_url='admin_login')
def delete_sales_notes(request, note_id):

    note_obj = Addsalesnotes.objects.get(id=note_id)
    note_obj.delete()

    messages.success(request, 'Note Removed Successfully...!')
    return redirect('/dashboard/sale-notes?u_id='+str(request.session.get('u_id')))
    del request.session['u_id']


@login_required(login_url='admin_login')
def get_sales_notes(request, cid):
    sales_notes = [{'note': salesnote.note, 'date_created': salesnote.added_on} for salesnote in Addsalesnotes.objects.filter(client_id=cid)]
    return JsonResponse({"data": sales_notes})

@login_required(login_url='admin_login')
def userdoc(request):
    d = Uploaddocument.objects.all()
    return render(request,'dashboard/temp/userdocuments.html',{'d':d})


@login_required(login_url='admin_login')
def partner(request):
    return render(request,'dashboard/temp/partner.html')

@login_required(login_url='admin_login')
def addcurrency(request):
    if request.method == 'POST':
        name = request.POST['name']
        ca = Addcurrency(name=name)
        ca.save()
        return redirect(addcurrency)
    else:
        context_data = {
        'ca':Addcurrency.objects.all()
        }
    return render(request,'dashboard/temp/addcurrency.html',context_data)
@login_required(login_url='admin_login')
def update_currency(request,id):
    if request.method == 'POST':
        a  = Addcurrency.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(addcurrency)
    return render(request,'dashboard/temp/addcurrency.html',{'a':a})


@login_required(login_url='admin_login')
def delete_currency(request, id):
    a = Addcurrency.objects.filter(id=id)
    a.delete()
    return redirect(addcurrency)


@login_required(login_url='admin_login')
def adddepartment(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        department = Adddepartment(name=name)
        department.save()
        return redirect(adddepartment)
    else:
        department = Adddepartment.objects.all()
    return render(request,'dashboard/temp/adddepartment.html',{'department':department})


@login_required(login_url='admin_login')
def update_department(request, id):

    if request.method == 'POST':
        a  = Adddepartment.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(adddepartment)
    return render(request,'dashboard/temp/adddepartment.html',{'a':a})


@login_required(login_url='admin_login')
def delete_department(request, id):
    a = Adddepartment.objects.filter(id=id)
    a.delete()
    return redirect(adddepartment)

@login_required(login_url='admin_login')
def addoffice(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        office = Addoffice(name=name)
        office.save()
        return redirect(addoffice)
    else:

        office = Addoffice.objects.all()

    return render(request,'dashboard/temp/addofice.html',{'office':office})


@login_required(login_url='admin_login')
def update_office(request,id):
    if request.method == 'POST':
        a  = Addoffice.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(addoffice)
    return render(request,'dashboard/temp/addofice.html',{'a':a})

@login_required(login_url='admin_login')
def delete_office(request, id):
    a = Addoffice.objects.filter(id=id)
    a.delete()
    return redirect(addoffice)

@login_required(login_url='admin_login')
def massmail(request):
    return render(request,'dashboard/temp/massmail.html')

@login_required(login_url='admin_login')
def addbrand(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        brand = Addbrand(name=name)
        brand.save()
        return redirect(addbrand)
    else:
       brand = Addbrand.objects.all()
    return render(request,'dashboard/temp/addbrand.html',{'brand':brand})

@login_required(login_url='admin_login')
def update_brand(request,id):
    if request.method == 'POST':
        a  = Addbrand.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(addbrand)
    return render(request,'dashboard/temp/addbrand.html',{'a':a})

def delete_brand(request, id):
    a = Addbrand.objects.filter(id=id)
    a.delete()
    return redirect(addbrand)

def addleadsregions(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        lead  = Addleadsregions(name=name)
        lead.save()
        return redirect(addleadsregions)
    else:
         lead = Addleadsregions.objects.all()
    return render(request,'dashboard/temp/addleadsregions.html',{'lead':lead})

def update_leadsregions(request,id):
    if request.method == 'POST':
        a  =Addleadsregions.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(addleadsregions)
    return render(request,'dashboard/temp/addleadsregions.html',{'a':a})

def delete_leadsregions(request, id):
    a = Addleadsregions.objects.filter(id=id)
    a.delete()
    return redirect(addleadsregions)

def addactype(request):
    if request.method == 'POST':
        name = request.POST['name']
        ac = Addaccounttype(name=name)
        ac.save()
        return redirect(addactype)
    else:
        context_data = {
        'ac':Addaccounttype.objects.all()
        }

    return render(request,'dashboard/temp/addactype.html',context_data)

def update_account_type(request,id):
    if request.method == 'POST':
        a  = Addaccounttype.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(addactype)
    return render(request,'dashboard/temp/addactype.html',{'a':a})

def delete_account_type(request, id):
    a = Addaccounttype.objects.filter(id=id)
    a.delete()
    return redirect(addactype)

def access_level(request):
    if request.method == 'POST':
        name = request.POST['name']
        al =  Access_level(name=name)
        al.save()
        return redirect(access_level)
    else:
        context_data = {
        'al':Access_level.objects.all()
        }

    return render(request,'dashboard/temp/access_level.html',context_data)

def update_access_level(request,id):
    if request.method == 'POST':
        a  = Access_level.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(access_level)
    return render(request,'dashboard/temp/access_level.html',{'a':a})

def delete_access_level(request, id):
    a = Access_level.objects.filter(id=id)
    a.delete()
    return redirect(access_level)

def leads_access_level(request):
    if request.method == 'POST':
        name = request.POST['name']
        al =  Leads_access_level(name=name)
        al.save()
        return redirect(leads_access_level)
    else:
        context_data = {
        'al':Leads_access_level.objects.all()
        }

    return render(request,'dashboard/temp/leads_access_level.html',context_data)

def update_leads_access_level(request,id):
    if request.method == 'POST':
        a  = Leads_access_level.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(leads_access_level)
    return render(request,'dashboard/temp/leads_access_level.html',{'a':a})


def delete_leads_access_level(request, id):
    a = Leads_access_level.objects.filter(id=id)
    a.delete()
    return redirect(leads_access_level)

def accounts(request):
    return render(request,'dashboard/temp/accounts.html')

class PendingDepositTemplateView(TemplateView):
    template_name = 'dashboard/temp/pendingdeposit.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PendingDepositTemplateView, self).get_context_data(*args, **kwargs)
        context['pending_deposits'] = UserDeposits.objects.filter(action_choice=0)
        return context

def pendingwithdraw(request):
    w = UserWithdraw.objects.filter(status=0)
    return render(request,'dashboard/temp/pendingwithdraw.html',{'w':w})

def internaltransfer(request):
    return render(request,'dashboard/temp/internaltransfer.html')

def withdraw(request):

    return render(request,'dashboard/temp/withdraw.html')

def user(request):
    return render(request,'dashboard/temp/user.html')

def roles(request):
    return render(request,'dashboard/temp/roles.html')

def permission(request):
    return render(request,'dashboard/temp/permission.html')

def ctclient(request):
    return render(request,'dashboard/temp/createclient.html')

def ctpartner(request):
    return render(request,'dashboard/temp/ctpartner.html')

def securityque(request):

    if request.method == 'POST':
        name = request.POST['name']
        sq = Securityque(name=name)
        sq.save()
        return redirect(securityque)
    else:
        context_data = {
        'sq':Securityque.objects.all()
        }
        return render(request,'dashboard/temp/securityque.html',context_data)


def update_securityque_type(request,id):

    if request.method == 'POST':
        a  = Securityque.objects.filter(id=id)
        name = request.POST['name']
        a.update(name=name)
        return redirect(securityque)
    return render(request,'dashboard/temp/securityque.html',{'a':a})


def delete_securityque_type(request, id):
    a = Securityque.objects.filter(id=id)
    a.delete()
    return redirect(securityque)


def register(request):
    r = Register.objects.all()
    return render(request,'dashboard/temp/register.html',{'r':r})


def login(request):
    if request.method=='POST':
        registers=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if register is not None:
            auth.login(request,registers)
            return redirect(dashboard)
        else:
            messages.info(request,'invalid credentials')
            return redirect(admin_login)
    else:
        return render(request,'dashboard/temp/login.html')


from apis.serializers import RegisterSerializer
class LiveAccountRetrieve(RetrieveAPIView):
    queryset=LiveAccount.objects.all()
    serializer_class=RegisterSerializer


class CreateUserTemplateView(TemplateView):
    template_name = 'dashboard/temp/crm_adduser.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CreateUserTemplateView, self).get_context_data(**kwargs)
        context['department'] = Adddepartment.objects.all()
        context['office'] = Addoffice.objects.all()
        context['brand'] = Addbrand.objects.all()
        context['accesslevel'] = Access_level.objects.all()
        context['leadsaccesslevel'] = Leads_access_level.objects.all()
        context['leadsregions'] = Addleadsregions.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        username_var = self.request.POST.get('uname')
        email_var = self.request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        if User.objects.filter(username=username_var).exists():
            return self.get(request, error="Username or email has been already taken", *args, **kwargs)
        if pwd1 != pwd2:
            return self.get(request, error="Password Don't Match", *args, **kwargs)
        user_obj = User.objects.create_user(username=username_var, password=pwd1, email=email_var)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        department = request.POST.get('department')
        office = request.POST.get('office')
        brandvisibility = request.POST.get('brandvisibility')
        accesslevel =  request.POST.get('accesslevel')
        leadaccesslevel = request.POST.getlist('leadsaccesslevel')
        leadsregions = request.POST.get('leadsregions')

        register = Agentusercreate(firstname=fname,lastname=lname, username=uname,email=email, department=department,
                   office=office,brandvisibility= brandvisibility,accesslevel= accesslevel,leadsaccesslevel =leadaccesslevel,
                   leadsregions= leadsregions,password=pwd1,confirmpassword=pwd2,user_id=user_obj.id)
        register.save()
        SalesAssignment.objects.create(agent=register)
        return redirect(agents)




class ClientdetailTemplateView(TemplateView):
    template_name = 'dashboard/temp/client.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ClientdetailTemplateView, self).get_context_data(**kwargs)
        context['country_names'] = Country.objects.all()
        return context



def updateagent(request,id):

    a  = Agentusercreate.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        department = request.POST['department']
        office = request.POST['office']
        brandvisibility = request.POST['brandvisibility']
        accesslevel = request.POST['accesslevel']
        leadsaccesslevel = request.POST['leadsaccesslevel']
        leadsregions = request.POST['leadsregions']

        a.update(firstname=fname,lastname=lname, username=uname,email=email,department=department,
            office=office,brandvisibility=brandvisibility,accesslevel=accesslevel,leadsaccesslevel=leadsaccesslevel,
            leadsregions=leadsregions)
        return redirect('agents')
    else:
        context = {}
        context['department'] = Adddepartment.objects.all()
        context['office'] = Addoffice.objects.all()
        context['brand'] = Addbrand.objects.all()
        context['accesslevel'] = Access_level.objects.all()
        context['leadsaccesslevel'] = Leads_access_level.objects.all()
        context['leadsregions'] = Addleadsregions.objects.all()
        context['ag'] = a
        return render(request,'dashboard/temp/updateagent.html', context=context)


# class DespositHistoryTemplateView(TemplateView):
#     template_name = "dashboard/temp/deposithistory.html"
#     custom_filter = ""

#     def get_context_data(self, *args, **kwargs):
#         context = super(DespositHistoryTemplateView, self).get_context_data(**kwargs)
#         qs =Transaction_Method.objects.filter(type=1)
#         if not self.request.GET.get('added_on'):
#             context['deposit_history'] = qs

#         elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) != 7:
#             d = aker()
#             value = d.change(int(self.request.GET.get('added_on')))
#             context['deposit_history'] = qs.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
#         else:
#             pass
#         return context


def exportFile(context, exporttype, t=None):

    title_headers = ["Date", "Trans ID", "Client ID", "Name", "Comment", "Batch No.", "Amount", "Currency"]
    data_list = context['deposit_history']
    total_N = len(data_list)
    total_trans = 0.00

    if exporttype == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Report_{}.pdf'.format(dt.now())
        buffer = io.BytesIO()
        report = ToPDF(buffer, 'A4')
        d_list = []
        for hist in data_list:
            for val in hist.values():
                d_list.append(val.values())
        pdf = report.output(d_list, title_headers)
        response.write(pdf)
        return response

    if exporttype == 'excel':
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename=Report_{dt.now()}.xls"
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Summary")
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for i in range(len(title_headers)):
            worksheet.write(0, i, title_headers[i], font_style)
        for idx, hist in enumerate(data_list):
            for val in hist.values():
                total_trans += float(val['amount'])
                for i, v in enumerate(val.values()):
                    worksheet.write(idx+1, i, v)

        if t == 1:
            worksheet.write(total_N+2, 5, "Total Deposits", font_style)
            worksheet.write(total_N+2, 6, total_trans, font_style)
        elif t == 2:
            worksheet.write(total_N+2, 5, "Total Withdrawal", font_style)
            worksheet.write(total_N+2, 6, total_trans, font_style)
        workbook.save(response)
        return response

    if exporttype == 'csv':
        rows = [title_headers,]
        for hist in data_list:
            for val in hist.values():
                rows.append(val.values())
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        # response['Transfer-Encoding'] = 'chunked'
        # response.charset = 'UTF-8'
        response['Content-Disposition'] = f'attachment; filename="Report_{dt.now()}.csv"'
        return response


def get_context_data1(request, t=None):

        context = {}
        wallet = None
        if t:
            qs = Transaction_Method.objects.filter(type=t).order_by('id')
        else:
            qs = Transaction_Method.objects.all().order_by('id')
            wallet = WalletFinance.objects.all().order_by('id')
        year_val = ''
        month_val = ''
        date_val = ''
        temp_list = []
        if not request.GET.get('added_on'):
            if wallet:
                for w in wallet:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]
                        split_data = sec_val.split('.')[0]
                        client_id = w.user.register.client_id

                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                        'id':w.t_id, 'client_id':client_id,'name':w.user.username,'comments':transfer_to,
                        'batch_number':'--','amount':w.amount,'currency':w.currency}))
                        
            for i in qs:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]
                split_data = sec_val.split('.')[0]
                comment = i.comments.name
                client_id = i.user.register.client_id
                if not t and i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif not t and i.type == '1':
                    comment = f"Deposit from {comment}"
                temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                'id':i.id, 'client_id':client_id,'name':i.user.username,'comments':comment,
                'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}))

        elif request.GET.get('added_on') and int(request.GET.get('added_on')) != 7:
            d = DateRangeMaker()
            value = d.change(int(request.GET.get('added_on')))
            # print('----------date----',value,d.today_date_obj.strftime('%Y-%m-%d %G:%i:%s'))

            transaction_query_details = qs.filter(added_on__range=[value, d.today_date_obj])
            print('----------date----',transaction_query_details)
            if wallet:
                wallet_query_details = wallet.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d %G:%i:%s')])
                for w in wallet_query_details:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]
                        split_data = sec_val.split('.')[0]
                        client_id = w.user.register.client_id

                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                        'id':w.t_id, 'client_id':client_id,'name':w.user.username,
                        'comments':transfer_to,'batch_number':'--','amount':w.amount,'currency':w.currency}))

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]
                split_data = sec_val.split('.')[0]
                comment = i.comments.name
                client_id = i.user.register.client_id

                if not t and i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif not t and i.type == '1':
                    comment = f"Deposit from {comment}"
                temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                'id':i.id, 'client_id':client_id,'name':i.user.username,'comments':comment,
                'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}))

        elif request.GET.get('added_on') and int(request.GET.get('added_on')) == 7:
            transaction_query_details = qs.filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
            if wallet:
                wallet_query_details = wallet.filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
                for w in wallet_query_details:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]
                        split_data = sec_val.split('.')[0]
                        client_id = w.user.register.client_id

                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                        'id':w.t_id, 'client_id':client_id,'name':w.user.username,'comments':transfer_to,
                        'batch_number':'--','amount':w.amount,'currency':w.currency}))

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]
                split_data = sec_val.split('.')[0]
                comment = i.comments.name
                client_id = i.user.register.client_id
                if not t and i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif not t and i.type == '1':
                    comment = f"Deposit from {comment}"
                temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(split_data), 
                'id':i.id, 'client_id':client_id,'name':i.user.username,'comments':comment,
                'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}))
        else:
            pass
        Transaction_list = [{t[0]: t[1]} for t in sorted(temp_list, key=lambda x: x[0])]
        context['deposit_history'] = Transaction_list
        return context


def depositHistoryExport(request, exporttype):
    return exportFile(get_context_data1(request, 1), exporttype, 1)


def withdrawHistoryExport(request, exporttype):
    return exportFile(get_context_data1(request, 2), exporttype, 2)


def transactionHistoryExport(request, exporttype):
    return exportFile(get_context_data1(request), exporttype)


class DespositHistoryTemplateView(TemplateView):

    template_name = "dashboard/temp/crm_deposit_history.html"

    def get_context_data(self, *args, **kwargs):

        context = super(DespositHistoryTemplateView, self).get_context_data(**kwargs)
        Transaction_list = []
        
        year_val = ''
        month_val = ''
        date_val = ''

        qs = Transaction_Method.objects.filter(type=1).order_by('-id')

        if not self.request.GET.get('added_on'):
            for i in qs:

                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment, 'batch_number':i.batch_number,'amount':i.amount,'currency':'USD'}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) != 7:

            d = DateRangeMaker()
            value = d.change(int(self.request.GET.get('added_on')))
            transaction_query_details = qs.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':"USD"}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) == 7:

            transaction_query_details = qs.filter(added_on__range=[self.request.GET.get('startDate'), self.request.GET.get('endDate')])

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2] 
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val), 
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':"USD"}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list
        else:
            pass
        return context


class WithdrawHistoryTemplateView(TemplateView):

    template_name = "dashboard/temp/crm_withdraw_history.html"

    def get_context_data(self, *args, **kwargs):

        context = super(WithdrawHistoryTemplateView, self).get_context_data(**kwargs)
        Transaction_list = []
        year_val = ''
        month_val = ''
        date_val = ''

        qs = Transaction_Method.objects.filter(type=2).order_by('-id')
        if not self.request.GET.get('added_on'):
            for i in qs:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]  
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''
                    
                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val), 
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) != 7:
            d = DateRangeMaker()
            value = d.change(int(self.request.GET.get('added_on')))
            transaction_query_details = qs.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2] 
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) == 7:
            transaction_query_details = qs.filter(added_on__range=[self.request.GET.get('startDate'), self.request.GET.get('endDate')])
            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]  
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                inner_dict[i.user.username] = {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val), 
                                            'id':i.id, 'client_id':i.user.register.client_id,'name':i.user.username,
                                            'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':i.currency.name}
                Transaction_list.append(inner_dict)
            context['deposit_history'] = Transaction_list
        else:
            pass
        return context


class TransactionHistoryTemplateView(TemplateView):
    template_name = "dashboard/temp/crm_transaction_history.html"

    # custom_filter = ""

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionHistoryTemplateView, self).get_context_data(**kwargs)
        qs = Transaction_Method.objects.all()
        wallet = WalletFinance.objects.all()
        year_val = ''
        month_val = ''
        date_val = ''
        temp_list = []
        if not self.request.GET.get('added_on'):
            if wallet:
                count = 0
                for w in wallet:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]
                        seconds_val = sec_val.split('.')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        client_id = w.user.register.client_id
                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val), 
                                                                'id':w.t_id, 'client_id':client_id,'name':w.user.username,
                                                                'comments':transfer_to,'batch_number':'--','amount':round(w.amount,2),'currency':w.currency}))
            
            for i in qs:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]   
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''

                try:
                    currency = i.currency.name
                except:
                    currency = ''

                if i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif i.type == '1':
                    comment = f"Deposit from {comment}"

                temp_list.append((f'{year_val}{month_val}{date_val}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                'id':i.id, 'client_id':i.user.register.client_id, 'name':i.user,
                'comments':comment,'batch_number':i.batch_number,'amount':round(i.amount,2),'currency':currency}))

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) != 7:
            d = DateRangeMaker()
            value = d.change(int(self.request.GET.get('added_on')))
            transaction_query_details = qs.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
            if wallet:
                wallet_query_details = wallet.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
                for w in wallet_query_details:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]  
                        seconds_val = sec_val.split('.')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        client_id = w.user.register.client_id

                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                        'id':w.t_id, 'client_id':client_id,'name':w.user.username,
                        'comments':transfer_to,'batch_number':'--','amount':w.amount,'currency':w.currency}))

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]   
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''
                try:
                    currency = i.currency.name
                except:
                    currency = ''

                client_id = i.user.register.client_id

                if i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif i.type == '1':
                    comment = f"Deposit from {comment}"
                temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                'id':i.id, 'client_id':client_id,'name':i.user.username,
                'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':currency}))

        elif self.request.GET.get('added_on') and int(self.request.GET.get('added_on')) == 7:
            transaction_query_details = qs.filter(added_on__range=[self.request.GET.get('startDate'), self.request.GET.get('endDate')])
            if wallet:
                wallet_query_details = wallet.filter(added_on__range=[self.request.GET.get('startDate'), self.request.GET.get('endDate')])
                for w in wallet_query_details:
                    if w.user != None:
                        inner_dict = {}
                        date_split = str(w.added_on).split(' ')[0]
                        time_split = str(w.added_on).split(' ')[1]
                        hour_val = time_split.split(':')[0]
                        minute_val = time_split.split(':')[1]
                        sec_val = time_split.split(':')[2]  
                        seconds_val = sec_val.split('.')[0]
                        year_val = date_split.split('-')[0]
                        month_val = date_split.split('-')[1]
                        date_val = date_split.split('-')[2]
                        client_id = w.user.register.client_id

                        if w.details.startswith('Transfer from'):
                           transfer_to = w.details.replace('Transfer from','Transfer from')
                        elif w.details.startswith('Transfer to'):
                           transfer_to = w.details.replace('Transfer to','Transfer to')
                        elif w.details.startswith('Transfer Out'):
                           transfer_to = w.details.replace('Transfer Out','Transfer Out')
                        elif w.details.startswith('Transfer IN'):
                           transfer_to = w.details.replace('Transfer IN','Transfer IN')
                        temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{w.t_id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                        'id':w.t_id, 'client_id':client_id,'name':w.user.username,
                        'comments':transfer_to,'batch_number':'--','amount':w.amount,'currency':w.currency}))

            for i in transaction_query_details:
                inner_dict = {}
                date_split = str(i.added_on).split(' ')[0]
                time_split = str(i.added_on).split(' ')[1]
                hour_val = time_split.split(':')[0]
                minute_val = time_split.split(':')[1]
                sec_val = time_split.split(':')[2]  
                seconds_val = sec_val.split('.')[0]
                year_val = date_split.split('-')[0]
                month_val = date_split.split('-')[1]
                date_val = date_split.split('-')[2]
                try:
                    comment = i.comments.name
                except:
                    comment = ''
                try:
                    currency = i.currency.name
                except:
                    currency = ''

                client_id = i.user.register.client_id
                if i.type == '2':
                    comment = f"Withdraw from {comment}"
                elif i.type == '1':
                    comment = f"Deposit from {comment}"
                temp_list.append((f'{year_val}{month_val}{date_val}{client_id}{i.id}', {'added_on_val':str(year_val)+'-'+str(month_val)+'-'+str(date_val)+' '+str(hour_val)+':'+str(minute_val)+':'+str(seconds_val),  
                'id':i.id, 'client_id':client_id,'name':i.user.username,
                'comments':comment,'batch_number':i.batch_number,'amount':i.amount,'currency':currency}))
        else:
            pass
        Transaction_list = [{t[0]: t[1]} for t in sorted(temp_list, key=lambda x: x[0])]
        context['deposit_history'] = Transaction_list
        return context


def add_money_to_wallet(request):
    
    docs = []
    current_amount = None
    wallet = ''
    message1 = None
    message2 = None
    message3 = None

    currency = Addcurrency.objects.all()
    comments = Comments.objects.all()
    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)
    user = get_object_or_404(User.objects.filter(id=user_id))
    user_wallet = UserWallet.objects.filter(user=user_id)
    # user_wallet_instance = get_object_or_404(UserWallet.objects.filter(user=user_id))

    try:
        for wallet in user_wallet:
            current_amount = wallet.amount
    except:
        current_amount = 0
        
    added_amount = request.POST.get('amount')
    # try:
    if added_amount:
        action_type_list = request.POST.getlist('action_type')
        action_type = action_type_list[0]

        comment_list = request.POST.getlist('comments')
        comment = comment_list[0]
        try:
            comment_instance = Comments.objects.get(id=int(comment))
        except:
            messages.warning(request, 'Comment data is missing..!')
        currency_list = request.POST.getlist('currency')
        currency = currency_list[0]
        try:
            entered_curr_instance = Addcurrency.objects.get(id=int(currency))
        except:
            messages.warning(request, 'provide a currency..!')
        # batch_number = request.POST.get('batch_number')

        if action_type == '1':
            if current_amount:
                final_amount = current_amount + float(added_amount)
                user_wallet.update(amount=final_amount)
                trans_group = Transaction_Method(
                    user=user,
                    type=action_type,
                    comments=comment_instance,
                    amount=added_amount,
                    currency=entered_curr_instance,
                    # batch_number=str(batch_number),
                    )
                trans_group.save()
                no = 10000 + trans_group.id
                trans_group.batch_number = 'D'+ str(no)
                # trans_group.batch_number = 'D100'+str(trans_group.id)
                trans_group.save() 
                return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
            else:
                final_amount = 0 + float(added_amount)
                user_wallet.update(amount=final_amount)
                trans_group = Transaction_Method(
                    user=user,
                    type=action_type,
                    comments=comment_instance,
                    amount=added_amount,
                    currency=entered_curr_instance,
                    # batch_number=str(batch_number),
                    )
                trans_group.save()
                no = 10000 + trans_group.id
                trans_group.batch_number = 'D'+ str(no)
                # trans_group.batch_number = 'D100'+str(trans_group.id)
                trans_group.save() 
                return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
        elif action_type == '2':
            try:
                user_document = Uploaddocument.objects.get(user=user_id)
                if user_document.approve == True:
                    final_amount = current_amount
                    if float(added_amount) > 0:
                        if float(added_amount) <= float(final_amount):
                            final_amount = current_amount - float(added_amount)
                            user_wallet.update(amount=final_amount)

                            trans_group = Transaction_Method(
                                user=user,
                                type=action_type,
                                comments=comment_instance,
                                amount=added_amount,
                                currency=entered_curr_instance,
                                # batch_number=str(batch_number),
                                )
                            trans_group.save()
                            no = 10000 + trans_group.id
                            trans_group.batch_number = 'W'+ str(no)
                            trans_group.save() 
                            return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
                        else:
                            return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
                    else:
                        return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
                else:
                    messages.error(request, 'The documents were not verified yet...!')
            except:
                messages.error(request, 'User not uploaded the documents..!')
                # return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
    try:
        docs = Uploaddocument.objects.get(user_id=user_id)
    except:
        pass
    return render(request, 'dashboard/temp/crm_add_wallet_amount.html', {
        'reg_data': reg_data, 
        'currency': currency,
        # 'user_document': user_document,
        'comments': comments,
        'wallet': wallet,
        # 'redirect_url': redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id'))),
        'docs':docs,
        })


def trans_history(request, exporttype=None):

    response_list = []
    user_id = request.GET.get('u_id')
    print('--------user id-----', user_id)
    
    try:
        wallet = UserWallet.objects.get(user_id=user_id)
    except:
        wallet = ''

    reg_data = Register.objects.get(user_id=user_id)
    trans_method = Transaction_Method.objects.filter(user_id=user_id).order_by('-id')

    try:
        docs = Uploaddocument.objects.get(user_id=user_id)
    except:
        docs = None

    if exporttype:
        title_headers = ["Date", "Trans ID", "Type", "Amount", "Currency", "Comment", "Batch Number"]
        for trans in trans_method:
            date_split = str(trans.added_on).split(' ')[0]
            time_split = str(trans.added_on).split(' ')[1]
            hour_val = time_split.split(':')[0]
            minute_val = time_split.split(':')[1]
            sec_val = time_split.split(':')[2]
            split_data = sec_val.split('.')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]

            if trans.type == '1':
                type_1 = 'Deposit'
            else:
                type_1 = 'Withdraw'

            dt = "{}-{}-{} {}:{}:{}".format(date_val, month_val, year_val, hour_val, minute_val, split_data)
            response_list.append([dt, trans.id, type_1, trans.amount, trans.currency.name, trans.comments.name, trans.batch_number])
        return exportData(response_list, exporttype, 'trans_history', title_headers)

    if request.GET.get('added_on') and int(request.GET.get('added_on')) != 7:
        d= DateRangeMaker()
        value = d.change(int(request.GET.get('added_on')))
        trans_method = trans_method.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])

    elif request.GET.get('added_on') and int(request.GET.get('added_on')) == 7:
        trans_method = trans_method.filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
    # except:
    #     trans_method = ''
    #     wallet = ''
    #     reg_data = ''
    #     docs = ''
    return render(request,'dashboard/temp/crm_client_transaction.html', {'reg_data':reg_data, 'trans_method':trans_method, 
                                                'docs':docs, 'wallet':wallet, 'id':user_id})


def ib_wallet_withdraw_money(request):

    url = f'{settings.IB_URL}/api/v1/ib_users'
    req = requests.get(url)
    req_json = req.json()
    ib_id = 0
    current_amount = None
    docs = []

    for user in req_json:
        user_id = request.GET.get('u_id')
        user_id = Register.objects.get(user__id=user_id)
        client_id = user_id.client_id
        if user['client_id'] == client_id:
            ib_id = user['ib_id']
            break

    detail_api = f'{settings.IB_PORTAL}/api/v1/get_commission/{ib_id}'
    req = requests.get(detail_api).json()
    ib_urls = f'{settings.IB_URL}/api/v1/ib_users/{ib_id}'
    try:
        ib_urls_data = requests.get(ib_urls).json()
    except:
        ib_urls_data = None

    if ib_urls_data:
        ib_email = ib_urls_data['email']
    else:
        ib_email = ''
        
    if req['commission']:
        wallet = req['commission'][0]['wallet']
        commission_id = req['commission'][0]['ib_id_id']
    else:
        wallet = 0.00

    # message1 = None
    # message2 = None
    # message3 = None
    currency = Addcurrency.objects.all()
    comments = Comments.objects.filter()
    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)
    user = get_object_or_404(User.objects.filter(id=user_id))
    user_wallet = UserWallet.objects.filter(user=user_id)
    # user_wallet_instance = get_object_or_404(UserWallet.objects.filter(user=user_id))
    user_document = Uploaddocument.objects.filter(user=request.GET.get('u_id'))
    for x in user_wallet:
        current_amount = x.amount
    added_amount = request.POST.get('amount')
    client_id = request.POST.get('client_id')

    if added_amount:
        action_type_list = request.POST.getlist('type', None)
        action_type = action_type_list[0]
        comment_list = request.POST.get('comments')
        comment = comment_list[0]
        comment_instance = Comments.objects.get(id=int(comment))
        currency_list = request.POST.get('type')
        currency = currency_list[0]
        entered_curr_instance = Addcurrency.objects.get(id=currency)
        wallet_update_url = f'{settings.IB_PORTAL}/api/v1/client_commission/{ib_id}'

        if action_type == '1':
            # try:
            #     user_document = Uploaddocument.objects.get(user=user_id)
            #     if user_document.approve == True:
            if float(added_amount) > 0:
                if float(wallet) >= float(added_amount) and float(wallet) > 0:
                    final_amount =  wallet - float(added_amount)
                    data = {'wallet': final_amount}
                    req = requests.put(wallet_update_url, data=data)
                    trans_method = transaction_ibmethod_mdl.objects.create(user=user, type=action_type, comments=comment_instance,
                                amount=float(added_amount), currency=entered_curr_instance, client_id = client_id)
                    trans_method.save()
                    no = 1000 + trans_method.id
                    trans_method.batch_number = 'IB-TR'+ str(no)
                    trans_method.save()

                    subject = "IB-Commission withdrawn"
                    body = "The Details are: \n\n"\
                        "Client ID: \t{}".format(ib_urls_data['client_id'])+'\n'+\
                        "IB ID: \t\t{}".format(ib_urls_data['ib_id'])+'\n'+\
                        "User Name: \t{}".format(ib_urls_data['uname'].upper())+'\n'+\
                        "Commission Withdrawn: {}".format(float(added_amount))+'\n'+\
                        "Remaining Balance: {}".format(round(final_amount, 2))

                    from_email = 'support@hme158.com'

                    send_mail(
                        subject,
                        body,
                        from_email,
                        [ib_email],
                        fail_silently=False,
                    )

                    return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
                else:
                    messages.error(request, 'Insufficient wallet balance...!')
            else:
                messages.error(request, 'Please enter a valid amount...!')
            #     else:
            #         messages.error(request, 'The documents were not verified yet...!')
            # #         # return redirect('/dashboard/user/history/?u_id='+str(request.GET.get('u_id')))
            # except:
            #     messages.error(request, 'User not uploaded the documents..!')
        # return redirect(client)
    try:
        docs = Uploaddocument.objects.get(user_id=user_id)
    except:
        pass

    return render(request, 'dashboard/temp/crm_ib_wallet.html', {'reg_data':reg_data, 'comments': comments, 'currency': currency, 'docs':docs,
                                        'wallet':x,})
        # 'currency': currency,
        # 'user_document': user_document,
        # 'comments': comments,
        # 'message1': message1,
        # 'message2': message2,
#        'message3': message3,
        # 'user_wallet': user_wallet,
        # 'ib_wallet': wallet
        # 'redirect_url': request.build_absolute_uri(reverse('client')),
        #})

    # return render(request,'dashboard/temp/ib_wallet_added_money.html')


def trans_Ibhistory(request):

    docs = []
    transaction = ''

    try:
        docs = Uploaddocument.objects.get(user_id=user_id)
    except:
        pass

    user_id = request.GET.get('u_id')
    reg_data = Register.objects.get(user_id=user_id)

    if not request.GET.get('added_on'):
        transaction = transaction_ibmethod_mdl.objects.filter(user=user_id)

    elif request.GET.get('added_on') and int(request.GET.get('added_on')) != 7:
        d = DateRangeMaker()
        value = d.change(int(request.GET.get('added_on')))
        transaction = transaction_ibmethod_mdl.objects.filter(user=user_id).filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])

    elif request.GET.get('added_on') and int(request.GET.get('added_on')) == 7:
        transaction = transaction_ibmethod_mdl.objects.filter(user=user_id).filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
    else:
        pass

    return render(request,'dashboard/temp/ib_trans_history.html', {'reg_data':reg_data, 'docs':docs, 'transaction':transaction, 'id':user_id})


def sales_assignment(request):

    countries = Country.objects.all()
    sales_queues = SalesQueue.objects.all()
    context = {'countries': countries, 'sales_queues': sales_queues}

    if request.POST:
        temp = {}
        for i in range(1, len(sales_queues) + 2):
            temp[i] = {}
            if request.POST.get(f"enabled_state_{i}"):
                temp[i]['enabled_state'] = 1
            else:
                temp[i]['enabled_state'] = 0
            if request.POST.get(f"default_state_{i}"):
                temp[i]['default_state'] = 1
            else:
                temp[i]['default_state'] = 0
            countries = request.POST.getlist(f"countries_{i}")
            if countries:
                country_list = ','.join(countries)
            else:
                country_list = SalesAssignment.objects.get(id=i).country_list
            temp[i]['country_list'] = country_list
            temp[i]['promo_code'] = request.POST.get(f"promo_code_{i}")
            sales_queue_id = request.POST.get(f"sales_queue_{i}")
            
            if sales_queue_id and sales_queue_id != 'None':
                sq = SalesQueue.objects.get(id=int(sales_queue_id))
            else:
                sq = None
            temp[i]['salesqueue'] = sq
        for key, value in temp.items():
            id = key
            sanm = SalesAssignment.objects.filter(id=id)
            sanm.update(enabled_state=value['enabled_state'], default_state=value['default_state'], country_list=value['country_list'], promo_code=value['promo_code'], sales_queues=value['salesqueue'])
        sales_assignments = SalesAssignment.objects.all()

    else:
        sales_assignments = SalesAssignment.objects.all()

    context['sales_assignments'] = sales_assignments
    return render(request,'dashboard/temp/crm_sales_assignment.html', context=context)
