from django.contrib import admin

from . models import *


@admin.register(UserWallet)
class UserWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'register', 'amount')


@admin.register(WalletFinance)
class WalletFinanceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'currency', 'feededucted', 'status')


@admin.register(LiveAccount)
class WalletFinanceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'account_no', 'ac_type', 'balance', 'group')


admin.site.register(Uploaddocument)
admin.site.register(UserDeposits)
admin.site.register(DemoAccount)
admin.site.register(UserWithdraw)
admin.site.register(UserDepositApproval)

# admin.site.register(LiveAccount)