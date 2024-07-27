# Generated by Django 4.2.2 on 2023-06-16 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control', '0008_club_short_name_alter_club_acronym_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='picture_url',
        ),
        migrations.AddField(
            model_name='manager',
            name='is_player',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='manager',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='manager',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='control.club'),
        ),
    ]