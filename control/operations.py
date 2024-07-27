from django.contrib.auth.models import User
from control.models import (
    Player, 
    Club, 
    Manager, 
    ClubJoinRequest)
from profiles.models import Picture

def get_context(request):
    context = dict()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        player = Player.objects.filter(user=user).first()
        if player: 
            context['my_club']=player.club
            context['player']=player
        pic = Picture.objects.get(user=user)
        if pic.is_uploaded: context['pic']=pic
        manager = Manager.objects.filter(user=user).first()
        join_req = ClubJoinRequest.objects.filter(user=user).first()
        if manager:
            context['req_count'] = len([
                c for c in ClubJoinRequest.objects.filter(club=manager.club, is_approved=False).all()
                ])
            context['my_club']=manager.club
            context['manager']=manager
        if join_req:
            context['my_requested_club']=join_req.club
            context['join_req']=join_req
                  
    return context