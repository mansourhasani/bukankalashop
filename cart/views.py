from django.shortcuts import render,redirect
from django.contrib import messages
from catalog.models import Commodity
from .models import *
from django.contrib.auth.decorators import login_required
from order.models import OrderForm

def cart_detail(request):
    cart=Cart.objects.filter(user_id=request.user.id)
    user=request.user
    form=OrderForm
    total=0
    for p in cart:
        total+=p.product.reduc_price * p.quantity
    return render(request,'cart/cart.html',{'cart':cart,'total':total,'form':form,'user':user})
    

@login_required(login_url='accounts:login')
def add_cart(request,id):
    url=request.META.get('HTTP_REFERER')
    product=Commodity.objects.get(id=id)
    data=Cart.objects.filter(user_id=request.user.id,product_id=id)
    if data:
        check='yes'
    else:
        check='no'

    if request.method=='POST':
        form=CartForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data['quantity']
            if check=='yes':
                shop=Cart.objects.get(user_id=request.user.id,product_id=id)
                shop.quantity+=info
                shop.save()
            else:
                Cart.objects.create(user_id=request.user.id,product_id=id,quantity=info)
                messages.success(request,'محصول به سبد خرید اضافه شد','success')
        return redirect(url)    

@login_required(login_url='accounts:login')
def remove_cart(request,id):
    url=request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)