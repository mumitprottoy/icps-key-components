# Generated by Django 4.2.2 on 2023-06-19 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_matchstarttime_matchpov_goal_against_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamstat',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
