# Generated by Django 4.2.11 on 2024-03-27 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0003_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
