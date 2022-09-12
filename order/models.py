import email
from django.db import models
from django.contrib.auth.models import User
from catalog.models import *
from django.forms import ModelForm
from django_jalali.db import models as jmodels

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    create=jmodels.jDateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    paid=models.BooleanField(default=False,verbose_name='وضعیت پرداخت')
    discount=models.PositiveIntegerField(blank=True,null=True,verbose_name='تخفیف')
    email=models.EmailField(verbose_name='ایمیل')
    f_name=models.CharField(max_length=200,verbose_name='نام')
    l_name=models.CharField(max_length=200,verbose_name='نام خانوادگی')
    address=models.CharField(max_length=1000,verbose_name='آدرس')


    def get_price(self):
        total=sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price=(self.discount/100)*total
            return int(total-discount_price)
        return total

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name='سفارش'
        verbose_name_plural = 'سفارشات' 

    
class ItemOrder(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item',verbose_name='سفارش')
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')   
    product=models.ForeignKey(Commodity,on_delete=models.CASCADE,verbose_name='محصول')
    quantity=models.IntegerField(verbose_name='تعداد')


    def __str__(self):
        return self.user.username

    def price(self):
        return self.product.reduc_price * self.quantity

    class Meta:
        verbose_name='اقلام سفارش'
        verbose_name_plural = 'اقلام سفارشات'    

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['email','f_name','l_name','address']
    
        


class Coupon(models.Model):
    name=models.CharField(max_length=100,unique=True,verbose_name='نام کد تخفیف')
    active=models.BooleanField(default=False,verbose_name='فعال')   
    start=jmodels.jDateTimeField(verbose_name='شروع طرح')
    end=jmodels.jDateTimeField(verbose_name='پایان اعتبار')
    discount=models.IntegerField(verbose_name='درصد تخفیف')

    class Meta:
        verbose_name='کد تخفیف'
        verbose_name_plural = 'کد تخفیف' 