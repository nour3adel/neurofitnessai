# Generated by Django 5.0.1 on 2024-02-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0024_userprofile_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verification_code',
            field=models.IntegerField(default=0, max_length=6),
        ),
    ]
