from django.db import models


#region[Red] Muscle Group  

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='MuscleGroup Name')  # Ensure names are unique
    image = models.ImageField(upload_to='muscleGroups_photos', default='muscleGroups_photos/1.png')
   
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Muscle Group'
        ordering = ['name']
    
#endregion

#region[Green] Muscle Group Workout   

class MuscleGroupWorkout(models.Model):
    
    msw_name = models.CharField(max_length=100,  verbose_name='MuscleGroupWorkout Name',default='f') 
    image = models.ImageField(upload_to='MuscleGroupWorkout_photos', default='MuscleGroupWorkout_photos/1.png')
    musclegroup = models.CharField(max_length=100,  verbose_name='MuscleGroup Name', default='n')  # Ensure names are unique
    
    def __str__(self):
        return self.msw_name

    class Meta:
        verbose_name = 'MuscleGroup Workout'
        ordering = ['msw_name']

     
#endregion

#region[White] Workout

class Workout(models.Model):
    name = models.CharField(max_length=100, verbose_name='Workout Name')
    protip = models.TextField(null=True, blank=True, verbose_name='Pro Tip')
    howto = models.TextField(null=True, blank=True, verbose_name='How To')
    equipments = models.TextField(null=True, blank=True, verbose_name='Equipments')
    primary_image = models.ImageField(upload_to='workouts_photos', default='workouts_photos/1.png')
    secondary_image = models.ImageField(upload_to='workouts_photos', default='workouts_photos/1.png')
    variations_image = models.ImageField(upload_to='workouts_photos', default='workouts_photos/1.png')
    alternatives_image = models.ImageField(upload_to='workouts_photos', default='workouts_photos/1.png')
    video = models.FileField(upload_to='workout_videos', null=True, blank=True, verbose_name='Workout Video', default='workouts_videos/1.mp4')
    musclegroup_workout = models.CharField(max_length=100, default='n')  # Ensure names are unique


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Workout'
        ordering = ['name'] 
 
#endregion