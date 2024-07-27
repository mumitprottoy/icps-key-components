from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import outsiders_only
from icps_lib.subroutines import validate_form_fields
from .operations import create_user, sign_in
from django.contrib.auth.models import User
from control.restrictions import profile_pic_required       
from .models import ActivationLink      

                                                        
@outsiders_only
def signup(request):
    context = dict()
    context['cr']='four-cr7.png'
    context['title']='Signup'
    if request.method=='POST':
        data = request.POST
        if validate_form_fields(
            inputs=list(dict(data).keys()), 
            fields=['first_name', 'last_name',
                    'username', 'email',
                    'password', 'confirm_password']
            ):
            response = create_user(data)
            if response[0]:
                context['activation_link']=True
                return render(request, 'link_sent.html', context)
            else:
                context['form_data']=data
                context['err_msg']=response[1]
    
    return render(request, 'signup.html', context)


@outsiders_only
def signin(request):
    context = dict()
    if request.method=='POST':
        data = request.POST
        if validate_form_fields(
            inputs=list(dict(data).keys()), 
            fields=['username', 'password']):
            user = User.objects.filter(username=data['username']).first()
            if user:
                response = sign_in(request, user, data['password'])
                if response['logged_in']:
                    return redirect('home')
                else:
                    if not user.is_active:
                        from .operations import send_activation_link
                        send_activation_link(user)
                        context['activation_link']=True
                        return render(request, 'link_sent.html', context)
                    context['err_msg']='Wrong Password.'
            else:context['err_msg']='Username does not exist.'
        else: context['err_msg']='Input data was corrupted.'
    return render(request, 'login.html', context)



def acivate_account(request, link):
    if ActivationLink.objects.filter(link=link).exists():
        act_link = ActivationLink.objects.get(link=link)
        from .operations import update_activation_link
        update_activation_link(act_link)
        user = act_link.user
        user.is_active=True
        user.save()
        from django.contrib.auth import login
        login(request, user)
        return redirect(f'/profile/{user.username}')
    return redirect('nope')
    

def magic_link(request, link):
    if ActivationLink.objects.filter(link=link).exists():
        act_link = ActivationLink.objects.get(link=link)
        from .operations import update_activation_link
        update_activation_link(act_link)
        user = act_link.user
        from django.contrib.auth import login
        login(request, user)
        return redirect('change-password')
    return redirect('nope')
    
    
@outsiders_only
def forgot_password(request):
    context = dict()
    if request.method=='POST':
        data=request.POST
        if validate_form_fields(
            inputs=list(dict(data).keys()),
            fields=['username']
        ):
            user = User.objects.filter(username=data['username']).first()
            if user:
                from .operations import send_activation_link
                send_activation_link(user, link_head='https://icps7.xyz/magic/', email_type='magic')
                context['magic_link']=True
                return render(request, 'link_sent.html', context)
            else: context['err_msg']='Username does not exist.'
        else: context['err_msg']='Funny!'
    
    return render(request, 'forgot_password.html', context)
                
    
