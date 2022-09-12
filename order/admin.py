from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


class ItemInline(admin.TabularInline):
    model=ItemOrder
    readonly_fields=['user','product','quantity','price']

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','email','f_name','l_name','address','create','paid','get_price']
    inlines=[ItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display=['name','active','start','end','discount']
    list_filter = (
        ('name',JDateFieldListFilter),
        )
  

admin.site.register(Order,OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon,CouponAdmin)
