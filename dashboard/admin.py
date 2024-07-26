from django.contrib import admin

from .models import *
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Agentusercreate)
admin.site.register(Addleadsregions)
admin.site.register(Addaccounttype)
admin.site.register(Addsalesnotes)
admin.site.register(Securityque)
admin.site.register(Addoffice)
admin.site.register(Addbrand)
admin.site.register(Comments)
admin.site.register(SalesQueue)
admin.site.register(Addcurrency)
admin.site.register(Adddepartment)
admin.site.register(SalesAssignment)
admin.site.register(Transaction_Method)
admin.site.register(transaction_ibmethod_mdl)

admin.site.register(BlogCategory)
admin.site.register(BlogSubCategory)

admin.site.register(Blog_Seo)
admin.site.register(BlogCategory_Seo)
admin.site.register(BlogSubCategory_Seo)

class BlogAdmin(SummernoteModelAdmin):
    model = Blog
    summernote_fields = ('description',)
    


admin.site.register(Blog,BlogAdmin)
# admin.site.register(Transaction_IbMethod)