from django.urls import path,include, re_path
from django.contrib import admin
from . import views
from django.views.generic import RedirectView

urlpatterns = (
    
    # path('',views.home, name='home'),
    path('logout',views.logout, name='logout'),
    path('tempapi/<mt4>/', views.tempAPI, name="tempAPI"),
    path('login_client',views.logins, name='login_client'),
    path('code/verification/',views.code_verification,name='code_verification'),

    path('about',views.about, name='about'),
    path('contact',views.contact, name='contact'),
    path('signup',views.UserSignupTemplateView.as_view(), name='signup'),
   
    path('assets',views.assets,name="assets"),
    path('partner',views.partner,name="partner"),
    path('deposit',views.deposit,name="deposit"),
    path('platform',views.platform,name="platform"),
    path('withdraw',views.withdraw,name="withdraw"),

    # path('user_mail_verify',views.user_mail_verify,name="usermailverify"),
    # re_path(r'^user_verify_link/(?P<user_id>\d+)/(?P<user_token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', views.VerifyUserToken.as_view(), name="VerifyUserToken"),

    path('clients-data',views.clients_data,name="clients_data"),
    # path('payments-data',views.payments_data,name="payments_data"),
    path('transferclient',views.transferClient,name='transferClient'),
    path('trades-data',views.trades_data,name="trades_data"),
    path('assignibtoclient',views.assignIBToClient,name='assignIBToClient'),
    path('dashboard-data',views.getIBAdminAndIBPortalCumulativeData,name='dashboard-data'),
    path('volume-data',views.VolumeCumulativeData,name='volume-data'),
    path('proceed-payout',views.proceed_payout,name='procees-payout'),
    
    
    path('home',views.Home.as_view(),name="home"),
    path('',views.test_login.as_view(),name="test_login"),

    path('overview',views.Why.as_view(),name="overview"),
    path('blog',views.Blogs.as_view(),name="blog"),
    path('blogcategory/<str:slug>',views.BlogsCategorys.as_view(),name="blogscategory"),
    path('blogdetail/<str:slug>',views.BlogDetail.as_view(),name="blogdetail"),
    path('deposits',views.Deposits.as_view(),name="deposits"),
    path('withdrawal',views.Withdrawal.as_view(),name="withdrawal"),
    path('getintouch',views.Getintouch.as_view(),name="getintouch"),
    path('registration',views.Registration.as_view(),name="registration"),
    path('ctrader-plateform',views.MT4.as_view(),name="mt4"),
    path('account-types',views.AccountType.as_view(),name="account-types"),

    # re_path(r'^en/.*/$', RedirectView.as_view(url='/en/')),
)