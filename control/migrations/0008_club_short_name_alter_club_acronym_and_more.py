# Generated by Django 4.2.2 on 2023-06-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_alter_player_kit_name_alter_player_kit_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='short_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='acronym',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='logo_url',
            field=models.TextField(default='https://images.icps7.xyz/clubs/default_club_logo.png'),
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
