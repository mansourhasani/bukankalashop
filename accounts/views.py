from django.urls import reverse
from contextlib import redirect_stderr
from lib2to3.pgen2 import token
from django.shortcuts import render,redirect,get_object_or_404
from catalog.models import profile
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from random import randint
# import ghasedak
from kavenegar import *
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from order.models import *


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.id)+text_type(timestamp))

email_generator=EmailToken()


def user_register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=User.objects.create_user(username=data['user_name'],email=data['email'],first_name=data['first_name'],
                                        last_name=data['last_name'],password=data['password_2'])
                user.is_active=False
                user.save()
                domain=get_current_site(request).domain
                uidb64=urlsafe_base64_encode(force_bytes(user.id))
                #url= reverse('accounts:active',kwargs={'uidb64':uidb64,'token':email_generator.make_token(user)})
                url = reverse('accounts:active',kwargs={'uidb64':uidb64,'token':email_generator.make_token(user)})
                link='http://' + domain + url
                email= EmailMessage(
                    'فعال سازی کاربر',
                    link,
                    'test<karzanboukan222@gmail.com>',
                    [data['email']]
                )
                email.send(fail_silently=False)
                messages.warning(request,' ثبت نام انجام شد ، لطفا برای تایید حساب کاربری به ایمیل خود مراجعه کنید','warning')
                return redirect('catalog:index')
            except:
                messages.warning(request,' ایمیل یا نام کاربری تکراری است','warning')
    else:
        form=UserRegisterForm()
    context={'form':form}
    return render(request,'accounts/register.html',context)

class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id=force_text(urlsafe_base64_decode(uidb64))
        print(id)
        user=User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')

def user_login(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:
                user=authenticate(request,username=User.objects.get(email=data['user_name']),password=data['password_1'])
            except:
                user=authenticate(request,username=data['user_name'],password=data['password_1'])
            if user is not None:
                login(request,user)
                messages.success(request,'شما با موفقیت وارد شدید','primary')
                return redirect('catalog:index')
            else:
                messages.success(request,'رمز یا نام کاربری وارد شده اشتباه است','danger')
    else:
        form=UserLoginForm()
    context={'form':form}
    return render(request,'accounts/login.html',context)


def user_logout(request):
    logout(request)   
    messages.success(request,'شما خارج شدید','primary')
    return redirect('catalog:index')

# class RegisterEmail(View):
#     def get(self,request):
#         return redirect('accounts:login')


@login_required(login_url='accounts:login')
def user_profile(request):
    prrofile=get_object_or_404(profile,user_id=request.user.id)
    return render(request,'accounts/profile.html',{'prrofile':prrofile})

    
@login_required(login_url='accounts:login')
def user_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'ویرایش پروفایل با موفقیت انجام شد','success')
            return redirect('accounts:profile')
            
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    context={'user_form':user_form,'profile_form':profile_form}
     
    return render(request,'accounts/update.html',context)


def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        profile_form=ProfileUpdateForm(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'رمز با موفقیت تغییر کرد','success')
            return redirect('accounts:profile')
        else:
            messages.error(request,' رمز به درستی وارد نشده است','danger')
            return redirect('accounts:change')

    else:
        form=PasswordChangeForm(request.user)
    context={'form':form}
    return render(request,'accounts/change_password.html',context)


def phone(request):
    if request.method=='POST':
        form=PhoneForm(request.POST)
        if form.is_valid():
            global random_code,phone
            data=form.cleaned_data
            phone=f"0{data['phone']}"
            random_code=randint(1000,9999)
            
            # message = "تست ارسال وب سرویس قاصدک"
            
            # linenumber = "30005088"
            # sms = ghasedak.Ghasedak("c03dee12dfa4c2e31e60f9c1384d58fa64730ae194f525f1f349483661591632")
            # sms.send({ 'message': message,'receptor' : phone, 'linenumber': linenumber  })

            
  
            api = KavenegarAPI('75426A5752476F39312F4A316663427965536B6A336270385A33376E6C61416932554A36637368307177343D')
            api.sms_send({ 'sender' : '10008663', 'receptor': phone, 'message' :random_code })
            #response = api.sms_send( params)messages.success(request,'خوش آمدید','success')
           
            #messages.success(request,'رمز با موفقیت تغییر کرد','success')
            return redirect('accounts:verify')
       
    else:
        form=PhoneForm()
    return render(request,'accounts/phone.html',{'form':form})




def verify(request):
    if request.method=='POST':
        form=CodeForm(request.POST)
        if form.is_valid():
            
            if random_code==form.cleaned_data['code']:
                prrofile=profile.objects.get(tel=phone)
                user=User.objects.get(profile__id=prrofile.id)
                login(request,user)
                
                return redirect('catalog:index')
            else:
                messages.success(request,'کد وارد شده اشتباه است','success')
    else:
        form=CodeForm()
    return render(request,'accounts/code.html',{'form':form})

def favourite(request):
    product=request.user.fa_user.all()
    return render(request,'accounts/favourite.html',{'product':product})

def history(request):
    data=Order.objects.filter(user_id=request.user.id)
    return render(request,'accounts/history.html',{'data':data})

class ResetPassword(auth_views.PasswordResetView):
    template_name='accounts/reset.html'
    success_url=reverse_lazy('accounts:reset_done')
    email_template_name='accounts/link.html'

class DonePassword(auth_views.PasswordResetDoneView):
    template_name='accounts/done.html'

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name='accounts/confirm.html'
    success_url=reverse_lazy('accounts:complete')

class Complete(auth_views.PasswordResetCompleteView):
    template_name='accounts/complete.html'
