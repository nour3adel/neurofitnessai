# Generated by Django 5.0.1 on 2024-02-08 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_history_user'),
        ('pages', '0036_user_is_active_user_is_staff_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pages.user'),
        ),
    ]
