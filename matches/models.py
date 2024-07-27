from django.db import models
from utils import constants
from entities.models import Club


class MatchDay(models.Model):
    date = models.DateField()
    
    def get_date_str(self) -> str:
        return self.date.strftime(constants.BASE_DATETIME_FORMAT)
    
    def __str__(self) -> str:
        return self.get_date_str()


class MatchTime(models.Model):
    hour = models.CharField(max_length=2)
    minute = models.CharField(max_length=2)
    
    def get_time_str(self) -> str:
        return f'{self.hour}:{self.minute}'
    
    class Meta:
        constraints = models.UniqueConstraint(
            name='unique_time',
            fields=['hour', 'minute']
        )
    
    def __str__(self) -> str:
        return self.get_time_str()


class Match(models.Model):
    home_side = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='home')
    away_side = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='away')
    
    class Meta:
        verbose_name_plural = 'Matches'
    
    def __str__(self) -> str:
        return f'{self.home_side.short_name} VS {self.away_side.short_name}'


class Fixture(models.Model):
    PLAYED = 'PLAYED'; TO_BE_PLAYED = 'TO BE PLAYED'; FORFEITED = 'FORFEITED'; CANCELED = 'CANCELED'
    MATCH_STATUS_CHOICES = (
        (PLAYED, PLAYED),
        (TO_BE_PLAYED, TO_BE_PLAYED),
        (FORFEITED, FORFEITED),
        (CANCELED, CANCELED)
    )
    
    # OneToMany because clubs can face again in knockout rounds
    club_match = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    date = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    time = models.ForeignKey(MatchTime, on_delete=models.CASCADE)
    status = models.CharField(max_length=24, choices=MATCH_STATUS_CHOICES, default=TO_BE_PLAYED)
    
    def __str__(self) -> str:
        return f'{self.date.str()} {self.time.str()} {self.club_match.str()}'
