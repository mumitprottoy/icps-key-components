from django.db import models
from django.contrib.auth.models import User
from utils import constants, exceptions


class ClubGroup(models.Model):
    name = models.CharField(max_length=1, unique=True, default='A')
    
    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=256, unique=True)
    acronym = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(ClubGroup, on_delete=models.CASCADE)
    logo_url = models.TextField(default=constants.DEFAULT_CLUB_LOGO_URL)
    
    def __str__(self) -> str:
        return self.name
            
    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username 
    
        
class Kit(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    number = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_kit_name_&_number_within_club',
                fields=['name', 'number'],
                condition=models.Q(player__club__isnull=False)
            )
        ]
    
    def __str__(self) -> str:
        return self.player.user.username
    
           
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs) -> None:
        if Player.objects.filter(
            user=self.user).exclude(club=self.club).exists():
            raise exceptions.ManagerFromAnotherClub()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.club.name
    

class JoinRequest(models.Model):
    MANAGER = 'MANAGER'; USER = 'USER'
    SENDER_TYPE_CHOICES = (
        (MANAGER, MANAGER),
        (USER, USER)
    )
    SENDER_TYPE_MODEL_MAP = {
        MANAGER: Manager,
        USER: User
    }
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=8, choices=SENDER_TYPE_CHOICES)
    sender_id = models.BigIntegerField()
    
    def approve(self):
        Player(user=self.user, club = self.club).save()
        self.delete()
    
    class Meta:
        constraints = models.UniqueConstraint(
            name='multiple_same_club_join_request',
            fields=['club', 'user'] 
        )
    
    def save(self, *args, **kwargs):
        if Player.objects.filter(user=self.user).exists():
            raise exceptions.SamePlayerMultipleClub()
        super().save(*args, **kwargs)
