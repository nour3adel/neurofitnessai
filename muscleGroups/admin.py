from django.contrib import admin
from .models import Workout,MuscleGroup,MuscleGroupWorkout
# Register your models here.

admin.site.register(Workout)
admin.site.register(MuscleGroup)
admin.site.register(MuscleGroupWorkout)


