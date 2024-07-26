from django.urls import path,include,re_path
from  . import views


urlpatterns = (

    path('permission',views.permission, name='permission'),
    path('createclient',views.ctclient, name='ctclient'),
    path('accounts',views.accounts, name='accounts'),
    path('withdraw',views.withdraw, name='withdraw'),
    path('partner',views.partner, name='partner'),
    path('',views.home, name='crm_home'),
    path('user',views.user, name='user'),
    path('roles',views.roles, name='roles'),
    path('createpartner',views.ctpartner, name='ctpartner'),
    path('addsecurity',views.securityque, name='securityque'),
    path('add_currency',views.addcurrency, name='addcurrency'),

    path('logout',views.admin_logout, name='admin_logout'),
    path('addoffice',views.addoffice,name='addoffice'),
    path('addbrand',views.addbrand,name="addbrand"),
    path('client',views.client, name='client'),
    path('login',views.login,name='admin_login'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('liveaccount',views.liveaccount,name='dashliveaccount'),
    path('adddepartment',views.adddepartment,name='adddepartment'),

    path('add_account_type',views.addactype, name='addactype'),
    path('dashfinance',views.finance,name='dashfinance'),
    path('documents/',views.documents,name='documents'),
    path('agents',views.agents,name='agents'),
    path('resend_email',views.resend_email,name='resend_email'),
    path('demoaccount',views.demoaccount,name='dashdemoaccount'),
    path('access_level',views.access_level, name='access_level'),
    path('adddepartment',views.adddepartment,name='adddepartment'),

    path('verify/email/<client_id>',views.verify_mail,name='verify_mail'),
    path('dashfinance/<exporttype>',views.finance,name='dashfinance'),
    path('updateagent/<int:id>',views.updateagent,name='updateagent'),
    path('pendingclients',views.pendingclients, name='pendingclients'),
    path('addsalesnotes',views.addsalesnotes,name='addsalesnotes'),
    path('user/history/',views.trans_history,name='trans_history'),
    path('pendingpartner',views.pendingpartner, name='pendingpartner'),
    path('update_brand/<int:id>',views.update_brand,name="update_brand"),
    path('delete_brand/<int:id>',views.delete_brand,name="delete_brand"),
    path('addleadsregions',views.addleadsregions,name='addleadsregions'),
    path('verify/documents',views.verify_document,name='verify_document'),

    path('delete_currency/<int:id>',views.delete_currency,name="delete_currency"),
    path('user/history/<exporttype>',views.trans_history,name='trans_history'),
    path('internaltransfer',views.internaltransfer, name='internaltransfer'),
    path('sales_assignment',views.sales_assignment,name='sales_assignment'),
    path('client/<int:pk>/delete',views.client_delete,name='client_delete'),
    path('pendingleverage',views.pendingleverage,name='pendingleverage'),
    path('user/ib/history/',views.trans_Ibhistory,name='trans_Ibhistory'),
    path('pendingwithdraw',views.pendingwithdraw, name='pendingwithdraw'),
    path('adduser',views.CreateUserTemplateView.as_view(), name='adduser'),
    path('client-update/<int:pk>',views.client_update,name='client_update'),
    path('update_office/<int:id>',views.update_office,name="update_office"),
    path('delete_office/<int:id>',views.delete_office,name="delete_office"),
    path('get_sales_notes/<cid>',views.get_sales_notes,name='get_sales_notes'),
    path('update_currency/<int:id>',views.update_currency,name='update_currency'),

    path('deposithistory',views.DespositHistoryTemplateView.as_view(),name='deposithistory'),
    path('pendingdeposit',views.PendingDepositTemplateView.as_view(), name='pendingdeposit'),
    path('update_account_type/<int:id>',views.update_account_type,name='update_account_type'),
    path('update_leadsregions/<int:id>',views.update_leadsregions,name="update_leadsregions"),
    path('delete_leadsregions/<int:id>',views.delete_leadsregions,name="delete_leadsregions"),
    path('update_department/<int:id>',views.update_department,name="update_department"),
    path('delete_department/<int:id>',views.delete_department,name="delete_department"),
    path('leads_access_level',views.leads_access_level, name='leads_access_level'),
    path('unverify/documents/',views.unverify_documents,name='unverify_documents'),
    path('add_money_to_wallet/',views.add_money_to_wallet,name='add_money_to_wallet'),
    re_path(r'^clientview/(?P<clientid>\d+)/$', views.clientview, name='clientprofile'),
    path('delete_access_level/<int:id>',views.delete_access_level,name="delete_access_level"),
    path('update_access_level/<int:id>,',views.update_access_level,name="update_access_level"),
    path('delete_account_type/<int:id>', views.delete_account_type,name="delete_account_type"),
    path('withdrawhistory',views.WithdrawHistoryTemplateView.as_view(),name='withdrawhistory'),

    path('delete_leads_access_level/<int:id>',views.delete_leads_access_level,name="delete_leads_access_level"),
    path('client_all_information/<int:client_id>',views.client_all_information,name='client_all_information'),
    path('delete_securityque_type/<int:id>',views.delete_securityque_type,name="delete_securityque_type"),
    path('update_securityque_type/<int:id>,',views.update_securityque_type,name='update_securityque_type'),
    path('transactionhistory',views.TransactionHistoryTemplateView.as_view(),name='transactionhistory'),
    path('withdraw/ib/wallet/money',views.ib_wallet_withdraw_money,name="ib_wallet_withdraw_money"),
    path('deposithistory/<exporttype>', views.depositHistoryExport,name='deposithistoryexport'),
    path('withdrawhistory/<exporttype>',views.withdrawHistoryExport,name='withdrawhistoryexport'),
    path('clientdetailfilter',views.ClientdetailTemplateView.as_view(), name='clientdetailfilter'),
    path('transactionhistory/<exporttype>',views.transactionHistoryExport,name='transactionhistoryexport'),
    path('update_leads_access_level/<int:id>,',views.update_leads_access_level,name="update_leads_access_level"),

    # path('user',views.register,name='user'),
    # path('mass_mail',views.massmail,name='massmail'),
    # path('notes',views.clientnotes,name='clientnotes'),
    # path('search/id/',views.search_by_id,name='search_by_id'),
    # path('user_documents',views.userdoc,name='user_documents'),
    # path('search/mt4/',views.search_by_mt4,name='search_by_mt4'),
    # path('search/name/',views.search_by_name,name='search_by_name'),
    # path('search/email/',views.search_by_email,name='search_by_email'),
    # path('verify/documents/',views.verify_document,name='verify_document'),
    #(r'^api/v1/live_accounts/(?P<pk>\d+)/$',views.LiveAccountRetrieve.as_view())
    # path('user/history/<int:client_id>',views.trans_history,name='trans_history'),
    # re_path(r'^demoaccount/(?P<id>\d+)/$', views.demoaccount, name='dashdemoaccount'),
)