# Generated by Django 4.2.2 on 2023-06-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activationlink',
            name='link',
            field=models.TextField(default='mxncb'),
        ),
    ]
