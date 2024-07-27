from django.shortcuts import render, redirect
from control.restrictions import login_required, profile_pic_required, only_players
from control.operations import get_context
from django.contrib.auth.models import User
from .models import Picture
from control.models import Player, Manager


@login_required
def set_profile_picture(request):
    context = get_context(request)
    if request.method=='POST':
        user = User.objects.get(username=request.user.username)
        pic_url = request.POST['pic_url']
        if pic_url:
            pic = Picture.objects.get(user=user)
            pic.is_uploaded=True
            pic.pic_url=pic_url
            pic.save()
            return redirect(f'/profile/{user.username}')
        context['err_msg']='No photo was chosen.'
    return render(request, 'set_profile_picture.html')



@profile_pic_required
def user_profile(request, username):
    context = get_context(request)
    user = User.objects.filter(username=username).first()
    if user:
        context['my_profile']=request.user.username==user.username
        context['user_']=user
        context['pic_']=Picture.objects.get(user=user)
        player = Player.objects.filter(user=user).first()
        manager = Manager.objects.filter(user=user).first()
        club=None
        if player:
            club=player.club 
            context['user_player']=player
        if manager: 
            club=manager.club
            context['user_manager']=manager
        if manager or player: context['user_club']=club
        return render(request, 'profile.html', context)
    
    return redirect('nope')

@profile_pic_required
def team_profile(request, team):
    context = get_context(request)
    from control.models import Club
    club = Club.objects.filter(short_name=team).first()
    if club:
        context['club']=club
        return render(request, 'club.html', context)
    
    return redirect('nope')


@login_required
@profile_pic_required
@only_players
def set_kit_name_and_number(request):
    context = get_context(request)
    user = User.objects.get(username=request.user.username)
    player = Player.objects.get(user=user)
    from teams.operations import get_available_kit_numbers
    if request.method=='POST':
        kit_name = request.POST['kit_name'].upper()
        kit_number = int(request.POST['kit_number'])
        if kit_number in get_available_kit_numbers(club=player.club):
            player.kit_name=kit_name
            player.kit_number=kit_number
            player.save()
            return redirect(f'/profile/{user.username}')
        else: context['err_msg']=f'Number {kit_number} already exists.'
    context['kit_numbers'] = get_available_kit_numbers(club=player.club)
    return render(request, 'kit.html', context)
    

@login_required
@profile_pic_required
def change_password(request):
    context = get_context(request)
    user = User.objects.get(username=request.user.username)
    
    if request.method=='POST':
        from icps_lib.subroutines import validate_form_fields
        data = request.POST
        if validate_form_fields(
            inputs=list(dict(data).keys()),
            fields=['password', 'confirm_password']
            ):
            pwd, conf_pwd = data['password'], data['confirm_password']
            from entrance.operations import check_password
            response = check_password(password=pwd, confirm_password=conf_pwd)
            if response[0]:
                user.set_password(pwd)
                user.save()
                from django.contrib.auth import logout
                logout(request)
                return render(request, 'password_changed.html', context)
            else: context['err_msg']=response[1]
        else: context['err_msg']='System faced a funny problem.'
    
    return render(request, 'change_password.html', context)

            
                