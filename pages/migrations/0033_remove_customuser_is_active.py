# Generated by Django 5.0.1 on 2024-02-07 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0032_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
    ]
