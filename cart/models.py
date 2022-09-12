from itertools import product
from django.db import models

from catalog.models import Commodity
from catalog.models import *
from django.forms import ModelForm

class Cart(models.Model):
    product=models.ForeignKey(Commodity,on_delete=models.CASCADE,verbose_name='محصول')
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    quantity=models.PositiveIntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name='خرید'
        verbose_name_plural = 'خرید ها'


class CartForm(ModelForm):
    class Meta:
        model=Cart
        fields=['quantity']