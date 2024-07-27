from django.shortcuts import redirect
from django.contrib.auth.models import User
from profiles.models import ProfilePicture


def allow_admins_only(view):
    def check_staffness(request, *args, **kwargs): # pun
        if request.user.is_staff:
            return view(request, *args, **kwargs)
        else: return redirect('home')        
    return check_staffness


def login_required(view):
    def check(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view(request, *args, **kwargs)
    return check


def self_uploaded_profile_pic_required(view):
    def check_pro_pic(request, *args, **kwargs):
        profile_pic = request.user.profilepicture
        if profile_pic.is_uploaded: 
            return view(request, *args, **kwargs)
    return check_pro_pic


def only_managers(view):
    def check_manager(request, *args, **kwargs):
        if hasattr(request.user, 'profilepicture'):
            return view(request, *args, **kwargs)
        return redirect('nope')
    return check_manager


def only_players(view):
    def check_player(request, *args, **kwargs):
        if hasattr(request.user, 'player'):
            return view(request, *args, **kwargs)
        return redirect('nope')
    return check_player


def only_staff(view):
    def check_staff(request, *args, **kwargs):
        if request.user.is_staff:
            return view(request, *args, **kwargs)
        return redirect('nope')
    return check_staff


