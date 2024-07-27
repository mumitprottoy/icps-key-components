from django.db import models


class Copy(models.Model):
    title=models.CharField(max_length=256, null=True, blank=True)
    html_id=models.CharField(max_length=256, null=True, blank=True)
    body=models.TextField()
    
    class Meta:
        verbose_name_plural='Copies'
    
    def __str__(self): return self.title
    
