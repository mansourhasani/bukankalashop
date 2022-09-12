from ast import mod
from itertools import product
from sre_constants import SUCCESS
from urllib import request
from xml.etree.ElementTree import Comment
from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.views import generic
from .filters import ProductFilter
from django.contrib import messages
from .form import *
from django.db.models import Q
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# class Index(generic.TemplateView):
#     template_name='catalog/index.html'

#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context['num_commidities']=models.Commodity.objects.all().count()
#         context['num_brands']=models.Brand.objects.all().count()
#         context['num_commidities_available']=models.Commodity.objects.filter(status='a').count()
#         context['num_users']=models.Users.objects.count()
#         return context

def Index(request,slug1=None,id=None):
    
    brand=Brand.objects.all()
    paginator=Paginator(brand,1)
    page_num=request.GET.get('page')
    try:
        page_obj=paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        page_obj = paginator.page(paginator.num_pages)
   
    if slug1:
        data=get_object_or_404(models.Brand,slug1=slug1,id=id)
        #products=products.filter(brand=data)
    classes=Classes.objects.filter(sub_clas=False)
    # products=models.Commodity.objects.all()
    #brand=models.Brand.objects.all()
    # if id:
    #     data=get_object_or_404(models.Classes,id=id)
    #     classes=products.filter(classes=data)
    return render(request,'catalog/index.html',{'classes':classes,'brand':page_obj,'page_num':page_num})

def all_product(request,slug=None,id=None):
    classes=Classes.objects.filter(sub_clas=False)
    products=Commodity.objects.all()
    paginator=Paginator(products,3)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    form=SearchForm()
    if 'search' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            data=form.cleaned_data['search']
            if data.isdigit():
                products=products.filter(Q(price__icontains=data)|Q(reduc_price__icontains=data))
            else:
                products=products.filter(Q(name__icontains=data))
    
    brand=Brand.objects.all()
    #brand=models.Brand.objects.all()
    if id and slug:
        
        data1=get_object_or_404(Brand,id=id,slug=slug)
        page_obj=products.filter(brand=data1)
        paginator=Paginator(page_obj,1)
        page_num=request.GET.get('page')
        page_obj=paginator.get_page(page_num)
    if id:
        data=get_object_or_404(Classes,id=id)
        page_obj=products.filter(classes=data)
        paginator=Paginator(page_obj,1)
        page_num=request.GET.get('page')
        page_obj=paginator.get_page(page_num)
    
    return render(request,'catalog/commodity_list.html',{'classes':classes,'products':page_obj
                    ,'page_num':page_num,'form':form,'brand':brand})
# class CommodityListView(generic.ListView):
#     model=models.Commodity
#     # products=models.Commodity.objects.all()
#     # filter=ProductFilter(request.GET,queryset=products)
#     # products=filter.qs
    
#     #return render(request,'catalog/commodity_list.html',{'filter':filter})
#     template_name='catalog/commodity_list.html'

def Commodity_Detail(request,slug1=None,id=None):
    commodity=get_object_or_404(Commodity,slug1=slug1,id=id)
    images=Images.objects.filter(product_id=id)
    comment_form=CommentForm()
    # cart=Cart.objects.filter(user_id=request.user.id)
    # cart_exist=True
    # for i in cart:
        
    #     if i.quantity==commodity.amount:
    #         cart_exist=False
    reply_form=ReplyForm()
    cart_form=CartForm()
    comment=Comment.objects.filter(product_id=id,is_reply=False)
    similar=commodity.tags.similar_objects()[:3]
    is_like=False
    if commodity.like.filter(id=request.user.id).exists():
        is_like=True
    
    is_unlike=False
    if commodity.unlike.filter(id=request.user.id).exists():
        is_unlike=True

    is_favourite=False
    if commodity.favourite.filter(id=request.user.id).exists():
        is_favourite=True
    return render(request,'catalog/commodity_detail.html',{'commodity':commodity,'similar':similar,
                        'is_like':is_like,'is_unlike':is_unlike,'comment_form':comment_form,
                        'comment':comment,'reply_form':reply_form,'images':images,'cart_form':cart_form,'is_favourite':is_favourite})


def all_brand(request):
    
    brand=Brand.objects.all()
    paginator=Paginator(brand,1)
    page_num=request.GET.get('page')
    try:
        page_obj=paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'catalog/brand_list.html',{'brand':page_obj,'page_num':page_num})
# class BrandListView(generic.ListView):
#     model=models.Brand
#     template_name='catalog/brand_list.html'

def product_like(request,id):
    url=request.META.get('HTTP_REFERER')
    product=get_object_or_404(Commodity,id=id)
    is_like=False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like=False
        messages.success(request,'نظر شما حذف شد','success')
    else:
        product.like.add(request.user)
        is_like=True
        messages.success(request,'نظر شما ثبت شد','warning')
    return redirect(url)

def product_unlike(request,id=None):
    url=request.META.get('HTTP_REFERER')
    product=get_object_or_404(Commodity,id=id)
    is_unlike=False
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
        is_unlike=False
        messages.success(request,'نظر شما حذف شد','danger')
    else:
        product.unlike.add(request.user)
        is_unlike=True
        messages.success(request,'نظر شما ثبت شد','dark')
    return redirect(url)


def product_comment(request,id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            data=comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'],rate=data['rate'],user_id=request.user.id,product_id=id)
            messages.success(request,'ممنون از اینکه نظر دادید','success')
            return redirect(url)
        else:
            return redirect(url)


def product_reply(request,id,comment_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        reply_form=ReplyForm(request.POST)
        if reply_form.is_valid():
            data=reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'],user_id=request.user.id,product_id=id,reply_id=comment_id,is_reply=True)
            messages.success(request,'ممنون که پاسخ دادید','primary')
            return redirect(url)
        else:
            return redirect(url)


def comment_like(request,id=None):
    url=request.META.get('HTTP_REFERER')
    comment=Comment.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
        messages.success(request,'نظر شما حذف شد','success')
    else:
        comment.comment_like.add(request.user)
        messages.success(request,'نظر شما ثبت شد','warning')
    return redirect(url)


def product_search(request):
    products=models.Commodity.objects.all()
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data['search']
            if data.isdigit():
                products=products.filter(Q(price__icontains=data)|Q(reduc_price__icontains=data))
            else:
                products=products.filter(Q(name__icontains=data))

            return render(request,'catalog/Commodity_list.html',{'products':products,'form':form})


def favourite_product(request,id):
    url=request.META.get('HTTP_REFERER')
    product=Commodity.objects.get(id=id)
    is_favourite=False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        is_favourite=False
        #messages.success(request,'از علاقه مندی های شما حذف شد','success')
    else:
        product.favourite.add(request.user)
        is_favourite=True
        #messages.success(request,'به لیست علاقه مندی های شما اضافه شد','warning')
    return redirect(url)


def contact(request):
    if request.method == 'POST':
        subject=request.POST['subject']
        email=request.POST['email']
        msg=request.POST['message']
        body=subject+'\n'+email+'\n'+msg
        form=EmailMessage(
            'ارتباط با ما',
            body,
            'bukankala.com',
            ('karzanboukan222@gmail.com',),
        )
        try:
            form.send(fail_silently=False)
        except:
            messages.success(request,'اتصال اینترنت خود را وصل کنید','warning')
    return render(request,'catalog/contact.html')