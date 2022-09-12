from dataclasses import fields
from distutils.command.upload import upload
from functools import total_ordering
from itertools import product
from multiprocessing.spawn import import_main_path
import re
from tabnanny import verbose
from tkinter.tix import Form
from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save #,post_delete,pre_delete,pre_save,m2m_changed
#from django.core.signals import request_finished,request_started
from phone_field import PhoneField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels


# Create your models here.

class Brand(models.Model):
    brand_name=models.CharField(max_length=200,verbose_name='نام برند')
    image = models.ImageField(upload_to='brand',verbose_name='تصویر')
    slug=models.SlugField(allow_unicode=True,unique=True,null=True,blank=True,verbose_name='عنوان')

    

    def __str__(self):
        
        return self.brand_name
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural = 'برندها' 



class Classes(models.Model):
    class_name=models.CharField(max_length=200,verbose_name='نام دسته بندی')
    sub_classes=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='sub',verbose_name='دسته بندی')
    sub_clas=models.BooleanField(default=False,verbose_name=' زیر دسته بندی ')
    #image = models.ImageField(upload_to='classes',null=True,blank=True)

    def __str__(self):
        
        return self.class_name

    def get_absolute_url(self):

        return reverse('catalog:classes',args=[str(self.id)],) 
    

    class Meta:
        verbose_name='دسته بندی'
        verbose_name_plural = 'دسته بندی ها' 
	
class Package_type(models.Model):
    package_name=models.CharField(max_length=200,verbose_name='نام بسته بندی')

    def __str__(self):
        
        return self.package_name
    

    class Meta:
        verbose_name='نوع بسته بندی'
        verbose_name_plural = 'نوع بسته بندی' 


# class Orders(models.Model):
#     user_id=models.ForeignKey('Users',on_delete=models.SET_NULL,null=True)
#     cost=models.PositiveIntegerField()
#     bank_name=models.CharField(max_length=200)
#     payment_type=models.CharField(max_length=200)
#     date_of_order=models.DateField(null=True,blank=True)
#     time_of_order=models.TimeField(null=True,blank=True)

    
    

# class Managers(models.Model):
#     first_name=models.CharField(max_length=200)
#     last_name=models.CharField(max_length=200)
#     address=models.CharField(max_length=1000)
#     tel=models.IntegerField()
#     user_name=models.CharField(max_length=200)
#     password=models.CharField(max_length=200)
    

# class Users(models.Model):
#     first_name=models.CharField(max_length=200)
#     last_name=models.CharField(max_length=200)
#     address=models.CharField(max_length=1000)
#     tel=models.IntegerField()
#     user_name=models.CharField(max_length=200)
#     email=models.CharField(max_length=200)
#     password=models.CharField(max_length=200)
#     id=models.UUIDField(primary_key=True,default=uuid.uuid4)

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر')
    address=models.CharField(max_length=1000,null=True,blank=True,verbose_name='آدرس')
    tel=PhoneField(null=True,blank=True,verbose_name='شماره تماس')

    def __str__(self):
        
        return self.user.username

    class Meta:
        verbose_name='پروفایل'
        verbose_name_plural = 'پروفایل ها'
    

class Commodity(models.Model):
    name=models.CharField(max_length=200,verbose_name='نام')
    slug1 =models.SlugField(allow_unicode=True,unique=True,null=True,blank=True,verbose_name='عنوان')
    brand=models.ForeignKey('Brand',on_delete=models.SET_NULL,null=True,verbose_name='برند')
    classes=models.ManyToManyField('Classes',blank=True,verbose_name='دسته بندی')
    tags=TaggableManager(blank=True,verbose_name='تگ')
    price=models.PositiveIntegerField(help_text="قیمت اصلی را وارد کنید",verbose_name='قیمت')
    reduc_price=models.PositiveIntegerField(help_text="قیمت  با تخفیف را وارد کنید",verbose_name='قیمت با تخفیف')
    #available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='commodity',verbose_name='تصویر')
    amount=models.PositiveIntegerField(null=True,verbose_name='موجودی')
    number_in_the_box=models.IntegerField(null=True,verbose_name='تعداد در بسته')
    weight=models.FloatField(null=True,verbose_name='وزن')
    package_type=models.ForeignKey('Package_type',on_delete=models.SET_NULL,null=True,verbose_name='نوع بسته بندی')
    information=RichTextField(blank=True,null=True,verbose_name='اطلاعات')
    like=models.ManyToManyField(User,blank=True,related_name='like_product',verbose_name='پسند')
    total_like=models.IntegerField(default=0,verbose_name='تعداد کل پسندها')
    unlike=models.ManyToManyField(User,blank=True,related_name='unlike_product',verbose_name='نپسندیدن')
    total_unlike=models.IntegerField(default=0,verbose_name='تعداد کل نپسندیدن ها')
    favourite=models.ManyToManyField(User,blank=True,related_name='fa_user',verbose_name='علاقه مندی')

    def average(self):
        data=Comment.objects.filter(is_reply=False,product=self).aggregate(avg=Avg('rate'))
        star=0
        if data['avg'] is not None:
            star=round(data['avg'],1)
        return star

    # class Meta:
        

    def total_like(self):
        
        return self.like.count()

    def total_unlike(self):
        
        return self.unlike.count()

    
    COMMODITY_STATUS=(
        ('m','موجود'),
        ('o','نا موجود'),
     
    )

    status=models.CharField(max_length=1,choices=COMMODITY_STATUS,blank=True,default='m',help_text="موجودی یا عدم موجودی کالا",verbose_name='وضعیت موجودی محصول')


    class Meta:
        ordering=["brand"]
        verbose_name='محصول'
        verbose_name_plural = 'محصولات'
    
    def get_absolute_url(self):

        return reverse('catalog:commodity_detail',args=[str(self.slug1),str(self.id)])  

    def __str__(self):
        
        return self.name 


def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user=profile(user=kwargs['instance'])
        profile_user.save()

post_save.connect(save_profile_user,sender=User)



class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    product=models.ForeignKey(Commodity,on_delete=models.CASCADE,verbose_name='محصول')
    comment=models.TextField(verbose_name='نظر')
    rate=models.PositiveBigIntegerField(default=1,verbose_name='رای')
    create=jmodels.jDateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    reply=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='comment_reply',verbose_name='پاسخ')
    is_reply=models.BooleanField(default=False,verbose_name='وضعیت پاسخ')
    comment_like=models.ManyToManyField(User,blank=True,related_name='com_like',verbose_name='نظر پسندیده')
    total_comment_like=models.PositiveBigIntegerField(default=0,verbose_name='تعداد پسند ها')

    def total_comment_like(self):
        return self.comment_like.count()

    def __str__(self):
        
        return self.comment

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name='نظر'
        verbose_name_plural = 'نظرات'


class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['comment','rate'] 


class ReplyForm(ModelForm):
    class Meta:
        model=Comment
        fields=['comment',]


class Images(models.Model):
    product=models.ForeignKey(Commodity,on_delete=models.CASCADE,verbose_name='محصول')
    name=models.CharField(max_length=100,blank=True,verbose_name='نام')
    image=models.ImageField(upload_to='image/',blank=True,verbose_name='تصویر')

    class Meta:
        verbose_name='تصویر'
        verbose_name_plural = 'تصاویر'