# Generated by Django 5.0.1 on 2024-02-05 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_userprofile_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
