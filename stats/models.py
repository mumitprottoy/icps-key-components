from django.db import models
from entities.models import Player
from matches.models import Fixture
from utils import exceptions


class Event(models.Model):
    name = models.CharField(max_length=16, unique=True) # Goal, Save, Assist, Yellow Card etc.


# Each point (positive or negative) to be gained per event by a player
class PointDistribution(models.Model):
    event = models.OneToOneField(Event, on_delete=models.Model)
    point = models.IntegerField()
    
    @classmethod
    def get_events(cls) -> list[Event]:
        return [pd.event for pd in cls.objects.all()]

    @classmethod
    def get_map(cls) -> dict[Event:int]:
        return {pd.event:pd.point for pd in cls.objects.all()}


class PlayerValidator:
    
    def __init__(self, player: Player, fixture: Fixture) -> None:
        self.player = player
        self.fixture = fixture
    
    def player_is_valid(self) -> bool:
        clubs = self.fixture.club_match.home_side, self.fixture.club_match.away_side
        
        for club in clubs:
            if club is self.player.club:
                return True
        return False


class EventTable(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    
    @classmethod
    def get_count(cls, event: Event, player: Player | None) -> int:
        kwargs = {'event': event}
        if player is not None: kwargs['player'] = player
        return cls.objects.filter(**kwargs).count()
    
    def save(self, *args, **kwargs):
        player_validator = PlayerValidator(self.player, self.fixture)
        if player_validator.player_is_valid():
            super().save(**args, **kwargs)
        raise exceptions.InvalidPlayer()
