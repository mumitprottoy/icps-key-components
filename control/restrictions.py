from django.shortcuts import redirect
from django.contrib.auth.models import User

def allow_admins_only(view):
    def check_staffness(request):
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


def profile_pic_required(view):
    def check_pro_pic(request, *args, **kwargs):
        if request.user.is_authenticated:
            from profiles.models import Picture
            user = User.objects.get(username=request.user.username)
            pic = Picture.objects.get(user=user)
            if not pic.is_uploaded: return redirect('set-profile-picture') 
        return view(request, *args, **kwargs)
    return check_pro_pic


def only_managers(view):
    def check_manager(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            from .models import Manager
            manager = Manager.objects.filter(user=user).first()
            if manager:
                return view(request, *args, **kwargs)
            return redirect('nope')
    return check_manager


def only_players(view):
    def check_player(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            from .models import Player
            player = Player.objects.filter(user=user).first()
            if player:
                return view(request, *args, **kwargs)
            return redirect('nope')
    return check_player


def only_staff(view):
    def check_staff(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            if user.is_staff:
                return view(request, *args, **kwargs)
            return redirect('nope')
    return check_staff


