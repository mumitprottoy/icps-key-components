# Generated by Django 4.2.2 on 2023-06-13 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Switches',
            },
        ),
    ]
