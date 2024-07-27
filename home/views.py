from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from control.models import Club
from control.restrictions import login_required, profile_pic_required
from icps_lib.subroutines import validate_form_fields, sign_in
from control.operations import get_context


@profile_pic_required
def home(request):
    context = get_context(request)
    from .models import Copy
    context['copy']=Copy.objects.get(title='About ICPS')
    context['teams']=[c for c in Club.objects.all()]
    return render(request, 'home.html', context)


from django.contrib.auth import logout
@login_required
def signout(request):
    logout(request)
    return redirect('login') 
    

@profile_pic_required
def nope(request):
    context = get_context(request)
    return render(request, 'nope.html', context)