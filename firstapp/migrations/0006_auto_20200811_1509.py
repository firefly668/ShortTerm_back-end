# Generated by Django 3.0.3 on 2020-08-11 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default=None, upload_to=''),
        ),
    ]
