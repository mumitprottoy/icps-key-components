from django.db import models
from django.contrib.auth.models import User
from profiles.models import Picture
from entrance.models import ActivationLink
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete



class ClubGroup(models.Model):
    name = models.CharField(max_length=1, unique=True, default='A')
    
    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=256, null=True)
    acronym = models.CharField(max_length=256, null=True)
    short_name = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(ClubGroup, on_delete=models.CASCADE, null=True)
    logo_url = models.TextField(default='https://images.icps7.xyz/clubs/default_club_logo.png')
    
    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    picture = models.ForeignKey(Picture, on_delete=models.DO_NOTHING, null=True, blank=True)
    kit_name = models.CharField(max_length=256, null=True, blank=True)
    kit_number = models.IntegerField(null=True, blank=True)
    is_captain = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    
    def __str__(self):
        captain = ' | Captain' if self.is_captain else ""
        manager = ' | Manager' if self.is_manager else ""
        return f"{self.user.username} : {self.club.name} {captain} {manager}"



class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    picture = models.ForeignKey(Picture, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_player = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} | {self.club.name}"


@receiver(pre_save, sender=Manager)
def manager_is_player(*args, **kwargs):
    manager = kwargs['instance']
    player = Player.objects.filter(user=manager.user).first()
    join_req = ClubJoinRequest.objects.filter(user=manager.user).first()
    if player:
        manager.is_player=True
        player.is_manager=True
        player.save()
    if join_req:
        if not join_req.is_approved:
            join_req.is_approved=True
            join_req.save()
   
   
    
@receiver(post_save, sender=Manager)
def manager_is_player(*args, **kwargs):
    manager = kwargs['instance']
    player=Player.objects.filter(user=manager.user).first()
    if manager.is_player:
        if not player:
            Player(user=manager.user, club=manager.club, is_manager=True).save()
    
    join_req = ClubJoinRequest.objects.filter(user=manager.user).first()
    if join_req:
        if not join_req.is_approved:
            join_req.is_approved=True
            join_req.save()
        



class Switch(models.Model):
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Switches'
    
    def __str__(self):
        return f"{self.name} : {self.active}"


class ClubAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} : {self.club.name}"


class ClubJoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    picture = models.ForeignKey(Picture, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        approved = ' | approved' if self.is_approved else ''
        return f"{self.user.username} | {self.club.name}{approved}"


@receiver(post_save, sender=ClubJoinRequest)
def join_request_approved(*args, **kwargs):
    join_req = kwargs['instance']
    if join_req.is_approved:
        if not Player.objects.filter(user=join_req.user).exists():
            Player(user=join_req.user, club=join_req.club).save()
    


@receiver(post_save, sender=Player)
def captain_changed(instance, created, *args, **kwargs):
    if not created and instance.is_captain:
        pl = instance
        for p in Player.objects.filter(club=pl.club).all():
            if (p != pl) and p.is_captain:
                p.is_captain=False
                p.save()
        
        
@receiver(post_save, sender=Player)
def player_already_created(*args, **kwargs):
    player = kwargs['instance']
    join_req = ClubJoinRequest.objects.filter(user=player.user).first()
    if join_req:
        if not join_req.is_approved:
            join_req.is_approved=True
            join_req.save()
    else:
        ClubJoinRequest(user=player.user, club=player.club, is_approved=True).save()
    
    
@receiver(post_delete, sender=Player)
def player_deleted(*args, **kwargs):
    user = kwargs['instance'].user
    ClubJoinRequest.objects.filter(user=user).all().delete()
    manager = Manager.objects.filter(user=user).first()
    if manager:
        if manager.is_player:
            manager.is_player=False
            manager.save()


@receiver(pre_save, sender=Player)
def add_pic_to_player(instance, *args, **kwargs):
    pic = Picture.objects.get(user=instance.user)
    instance.picture=pic
    
    
    
@receiver(pre_save, sender=Manager)
def add_pic_to_manager(instance, *args, **kwargs):
    pic = Picture.objects.get(user=instance.user)
    instance.picture=pic
    
    
@receiver(pre_save, sender=ClubJoinRequest)
def add_pic_to_join_request(instance, *args, **kwargs):
    pic = Picture.objects.get(user=instance.user)
    instance.picture=pic
    
    