# Generated by Django 5.0.3 on 2024-04-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0004_alter_file_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]