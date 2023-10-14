from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Sell_Car_Record)
class SellCarRecordDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','sell_car_id']