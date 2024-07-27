from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from control.models import Club, Player, Manager, ClubJoinRequest
from icps_lib.subroutines import validate_form_fields
# from control.switches import SQUAD_CHANGE_IS_ACTIVE
from control.restrictions import profile_pic_required, login_required, only_managers
from control.operations import get_context


@login_required
@profile_pic_required
def join_club(request):
    context = get_context(request)
    user = User.objects.get(username=request.user.username)
    print('Same user object:',request.user is user)
    if sum([
        int(ClubJoinRequest.objects.filter(user=user).exists()),
        int(Player.objects.filter(user=user).exists()),
        int(Manager.objects.filter(user=user).exists()),
    ])==0:
        if request.method=='POST':
            club = Club.objects.filter(short_name=request.POST['short_name']).first()
            if club:
                ClubJoinRequest(user=user, club=club).save()
                return redirect(f'/profile/{user.username}')
            else: context['err_msg']="Funny!"
        context['clubs']=[club for club in Club.objects.all()]
        return render(request, 'join_club.html', context)
    
    return redirect('nope')
    



@login_required
@profile_pic_required
def delete_join_request(request):
    join_req = ClubJoinRequest.objects.filter(user=request.user).first()
    if join_req:
        join_req.delete()
        return redirect(f'/profile/{request.user.username}')
    
    return redirect('nope')


@login_required
@profile_pic_required
def leave_club(request, team):
    club = Club.objects.filter(short_name=team).first()
    if club:
        player = Player.objects.filter(user=request.user, club=club).first()
        if player:
            player.delete()
            return redirect(f'/profile/{request.user.username}')
    return redirect('nope')


@profile_pic_required
def list_squad(request, team):
    context = get_context(request)
    club = Club.objects.filter(short_name=team).first()
    if club:
        context['squad'] = [p for p in Player.objects.filter(club=club).all()]
        context['captain'] = Player.objects.filter(club=club, is_captain=True).first()
        context['squad_manager'] = Manager.objects.filter(club=club).first()
        if context['squad_manager'] and context['captain']:
            if context['squad_manager'].user.username==context['captain'].user.username:
                context['manager_is_captain']=True
        context['club']=club
        return render(request, 'squad.html', context)
         
    return redirect('nope')


@login_required
@profile_pic_required
def squad_full(request):
    return render(request, 'squad-full.html')


@login_required
@profile_pic_required
@only_managers
def list_join_requests(request, team):
    context = get_context(request)
    club = Club.objects.filter(short_name=team).first()
    if club:
        join_reqs = [j for j in ClubJoinRequest.objects.filter(club=club, is_approved=False).all()]
        context['join_reqs']=join_reqs
        context['req_count']=len(join_reqs)
        return render(request, 'request_list.html', context)
    return redirect('nope')
    

@login_required
@profile_pic_required
def approve_join_request(request, join_id):
    join_req = ClubJoinRequest.objects.filter(id=join_id).first()
    club = join_req.club
    player_count_valid = len([p for p in Player.objects.filter(club=club).all()])<16
    if join_req and player_count_valid:
        join_req.is_approved=True
        join_req.save()
        return redirect(f'/join-requests/{club.short_name}')
    
    return redirect('nope')



@login_required
@profile_pic_required
def reject_join_request(request, join_id):
    join_req = ClubJoinRequest.objects.filter(id=join_id).first()
    club = join_req.club
    if join_req:
        join_req.delete()
        return redirect(f'/join-requests/{club.short_name}')
    
    return redirect('nope')


@login_required
@profile_pic_required
@only_managers
def set_captain(request):
    context = get_context(request); user = request.user
    manager = Manager.objects.get(user=user)
    players = [p for p in Player.objects.filter(club=manager.club, is_captain=False).all()]
    context['players'] = players
    
    if request.method=='POST':
        player_id = int(request.POST['player_id'])
        player = Player.objects.filter(id=player_id, club=manager.club).first()
        if player:
            player.is_captain=True
            player.save()
            return redirect(f'/teams/squad/{player.club.short_name}')
        else: context['err_msg']='Invalid player'
    
    return render(request, 'set_captain.html', context)
                    
