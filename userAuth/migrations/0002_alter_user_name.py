# Generated by Django 4.2.11 on 2024-03-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
    ]
