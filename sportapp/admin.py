from django.contrib import admin

from .models import *


class RegisterAdmin(admin.ModelAdmin):
   
    list_display = ('fname', 'client_id',)
    list_filter = ('country',)


admin.site.register(Contact)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Profile)
admin.site.register(Emailtemplate)
admin.site.register(RegisterUserCampaign)
admin.site.register(Addpage)
admin.site.register(Page_Seo)