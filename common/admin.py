from django.contrib import admin
from .models import *


@admin.register(Country)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')