from django.urls import path,include,re_path

from . import views


urlpatterns = (
    
    path('otp/',views.otp,name='otp'),
    path('usdt', views.usdt, name="usdt"),
    path('',views.profile, name='profile'),
    
    path('profile',views.profile,name='profile'),
    path('support',views.support, name='support'),

    path('addemail',views.addemail,name='addemail'),
    path('settings',views.settings,name='settings'),
    path('myaccount',views.myaccount,name='myaccount'),
    path('call_edit',views.call_edit,name='call_edit'),
    path('address',views.addaddress,name='addaddress'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('deposit_client',views.deposit, name='cldeposit'),
    path('open_liveac',views.laccount, name='liveaccount'),
    path('open_demoac',views.daccount, name='demoaccount'),
    path('prformance',views.performance, name='performance'),
    path('withdraw_client',views.withdraw, name='clwithdraw'),
    path('client_dash',views.client_dash, name='client-dash'),
    path('manage_funds',views.manage_funds,name='manage_funds'),
    path('download_plateform',views.downplat, name='dplateform'),

    path('deposit_skrill',views.deposit_skrill,name='deposit_skrill'),
    path('wallet_finance',views.wallet_finance,name='wallet_finance'),
    path('depositsuccess',views.depositsuccess, name='depositsuccess'),
    path('changepassword',views.changepassword, name='changepassword'),
    path('depositfailure',views.depositfailure, name='depositfailure'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('deposit_divepay',views.deposit_divepay,name='deposit_divepay'),
    path('user/withdraw/usdt', views.usdt_withdraw, name="usdt_withdraw"),
    path('forget-password/',views.forget_password,name='forget_password'),
    path('upload_documents/',views.upload_document,name='upload_document'),
    path('set_language/<language>',views.set_language,name='set_language'),
    path('deposit_neteller',views.deposit_neteller,name='deposit_neteller'),
    path('withdraw_divepay',views.withdraw_divepay,name='withdraw_divepay'),
    path('account_overview',views.account_overview,name='account_overview'),
     path('bitcoin_payment', views.bitcoin_payment, name="bitcoin_payment"),

    path('user/withdraw/bitcoin', views.bitcoin_withdraw, name="bitcoin_withdraw"),
    path('wallet_finance/<exporttype>',views.wallet_finance,name='wallet_finance'),
    path('demo/successful/',views.demo_account_response,name='live_account_response'),
    path('live/successful/',views.live_account_response,name='live_account_response'),

    path('divepay_failure', views.DepositFailureTemplateView.as_view(), name="DepositFailureTemplateView"),
    path('divepay_success', views.DepositSuccessTemplateView.as_view(), name="DepositSuccessTemplateView"),
    path('live_account_detail', views.GetLiveAccountDetailsView.as_view(), name="GetLiveAccountDetailsView"),
    path('demo_account_detail', views.GetDemoAccountDetailsView.as_view(), name="GetDemoAccountDetailsView"),
    path('live_account_reset_password', views.live_account_reset_password, name="live_account_reset_password"),
    path('account_details/', views.account_details, name="account_details"),
    path('country/', views.country_api_call, name="country_api_call"),
    path('client-trade-history', views.client_trade_history, name="client_trade_history"),
    path('client-trade-position', views.client_trade_position, name="client_trade_position"),


    path('client-trade-history', views.client_trade_history, name="client_trade_history"),
    path('client-trade-position', views.client_trade_position, name="client_trade_position"),


    # path('mail_test', views.testing_mail),
    # path('edit_documents/<int:pk>',views.edit_documents,name='edit_documents'),
    # path('profileupdate',views.profileupdate,name='profileupdate'),
)