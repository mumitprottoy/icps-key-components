from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_uploaded = models.BooleanField(default=False)
    url = models.TextField(default='https://images.icps7.xyz/profile/default.jpg')
    
    def __str__(self):
        uploaded = ' | uploaded' if self.is_uploaded else ""
        return self.user.username + uploaded


from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete


@receiver(post_save, sender=User)
def create_picture_with_every_user(instance, *args, **kwargs):
    if not Picture.objects.filter(user=instance).exists():
        Picture(user=instance).save()  

    
    
