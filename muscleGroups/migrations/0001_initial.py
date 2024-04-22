# Generated by Django 5.0.1 on 2024-02-06 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MuscleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='MuscleGroup Name')),
                ('image', models.ImageField(default='muscleGroups_photos/1.png', upload_to='muscleGroups_photos')),
            ],
            options={
                'verbose_name': 'Muscle Group',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MuscleGroupWorkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='MuscleGroupWorkout_photos/1.png', upload_to='MuscleGroupWorkout_photos')),
            ],
            options={
                'verbose_name': 'MuscleGroup Workout',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Workout Name')),
                ('protip', models.TextField(blank=True, null=True, verbose_name='Pro Tip')),
                ('howto', models.TextField(blank=True, null=True, verbose_name='How To')),
                ('equipments', models.TextField(blank=True, null=True, verbose_name='Equipments')),
                ('primary_image', models.ImageField(default='workouts_photos/1.png', upload_to='workouts_photos')),
                ('secondary_image', models.ImageField(default='workouts_photos/1.png', upload_to='workouts_photos')),
                ('variations_image', models.ImageField(default='workouts_photos/1.png', upload_to='workouts_photos')),
                ('alternatives_image', models.ImageField(default='workouts_photos/1.png', upload_to='workouts_photos')),
                ('video', models.FileField(blank=True, default='workouts_videos/1.mp4', null=True, upload_to='workout_videos', verbose_name='Workout Video')),
                ('musclegroup_workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muscleGroups.musclegroupworkout')),
            ],
            options={
                'verbose_name': 'Workout',
                'ordering': ['name'],
            },
        ),
    ]
