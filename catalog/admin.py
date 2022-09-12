from django.contrib import admin
from . import models
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model=models.Images
    extra=2 


@admin.register(models.Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'reduc_price','image', 'number_in_the_box', 'weight', 'package_type')
    list_filter = ('brand', 'classes')
    list_editable=('price','reduc_price')
    raw_id_fields=('classes',)
    inlines=[ImageInlines]

    fieldsets = (
        ('اطلاعات', {
            'fields': ('name','slug1', 'brand','amount', 'tags','image','like','unlike','classes', 'price', 'reduc_price','number_in_the_box', 'weight', 'package_type', 'information')
        }),
        ('موجود بودن', {
            'fields': ('status',)
        }),
    )
    prepopulated_fields= {
        'slug1':('name',)
    }


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tel', 'address')
    #list_filter = ('brand', 'classes')
admin.site.register(models.profile,ProfileAdmin) 

@admin.register(models.Brand)  
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    prepopulated_fields= {
        'slug':('brand_name',)
    }
    def __str__(self):

        return self.brand_name
    

@admin.register(models.Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('class_name','sub_classes',)

@admin.register(models.Package_type)
class Package_typeAdmin(admin.ModelAdmin):
    list_display = ('package_name',)   

# @admin.register(models.Managers)
# class ManagersAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'address', 'tel', 'user_name', 'password')
    
#     fieldsets = (
#         ('اطلاعات', {
#             'fields': ('first_name', 'last_name', 'user_name','password')
#         }),
        
#     )

# @admin.register(models.Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('id','first_name', 'last_name', 'address', 'tel', 'user_name', 'email', 'password')
    
#     fieldsets = (
#         ('اطلاعات', {
#             'fields': ('first_name', 'last_name', 'user_name','password')
#         }),
        
#     )


# @admin.register(models.Orders)
# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('cost', 'bank_name', 'payment_type', 'date_of_order', 'time_of_order')
#     list_filter = ('date_of_order', 'bank_name')
    
#     fieldsets = (
#         ('اطلاعات', {
#             'fields': ('cost', 'bank_name', 'payment_type', 'date_of_order', 'time_of_order')
#         }),
#     )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'create', 'rate')


# class ImageInlines(admin.TabularInline):
#     model=models.Images
#     extra=2 

@admin.register(models.Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'image')
