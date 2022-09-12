from time import time
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse
import requests
import json
import jdatetime

def order_detail(request,order_id):
    order=Order.objects.get(id=order_id) 
    form=CouponForm()   
    return render(request,'order/order.html',{'order':order,'form':form})


def order_create(request):
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            order=Order.objects.create(user_id=request.user.id,email=data['email'],
                                f_name=data['f_name'],l_name=data['l_name'],address=data['address'])
            messages.success(request,'سفارش شما با موفقیت ثبت گردید','success')
            cart=Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id,user_id=request.user.id,
                                        product_id=c.product_id,quantity=c.quantity)
            # Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:order_detail',order.id)

@require_POST
def coupon_order(request,order_id):
    form=CouponForm(request.POST)
    time=jdatetime.datetime.now()
    if form.is_valid():
        code=form.cleaned_data['code']
        try:
            coupon=Coupon.objects.get(name__iexact=code,start__lte=time,end__gte=time)
        except Coupon.DoesNotExist:
            messages.success(request,'کد تخفیف وارد شده یا اشتباه است و یا منقضی شده است','warning')
            return redirect('order:order_detail',order_id)
        order=Order.objects.get(id=order_id)
        order.discount=coupon.discount
        order.save()
    return redirect('order:order_detail',order_id)   


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order:verify/'


def send_request(request,price,order_id):
    global amount
    amount=price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": request.user.email}
    }

    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        #این 8  خط کد پایین باید بعد از شرط برابر با 100 تابع پایین باشد و order_id در یک متغیر گلوبال ذخیره شود
        order=Order.objects.get(id=order_id)
        order.paid=True
        order.save()
        cart=ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            product=Commodity.objects.get(id=c.product.id)
            product.amount-=c.quantity
            product.save()

        e_code = req.json()['errors']['code']
        messages.success(request,'کد تخفیف وارد شده یا اشتباه است و یا منقضی شده است','warning')
        return HttpResponse(f"Error code: {e_code},پرداخت انجام نشد")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('پرداخت با موفقیت انجام شد.')
            elif t_status == 101:
                return HttpResponse('تراکنش تکراری است : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('پرداخت ناموفق بود.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('پرداخت ناموفق بود و یا توسط کاربر لغو شد')