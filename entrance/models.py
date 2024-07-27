from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from icps_lib.uniqueness import unique_key


class ActivationLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.TextField(default='youjustmadeamistake')
    
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_activation_link_with_every_user(instance, *args, **kwargs):
    if not ActivationLink.objects.filter(user=instance).exists(): 
        ActivationLink(user=instance, link=unique_key(69)+instance.username).save() 