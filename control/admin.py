from django.contrib import admin
from .models import Club, Player, Switch, ClubAdmin, Manager, ClubGroup, ClubJoinRequest

admin.site.register([
    Club,
    Player,
    Switch,
    ClubAdmin,
    Manager,
    ClubGroup,
    ClubJoinRequest
])
