from django.shortcuts import render
from .models import MuscleGroup,Workout,MuscleGroupWorkout
# Create your views here.

def workouts(request,pk):
    user_info = request.session.get('user_info', None)
    try:
        workouts = Workout.objects.filter(id=pk)

    except Workout.DoesNotExist:
        workouts = None
    return render(request, 'muscleGroups/workout.html', {'user_info': user_info,'workouts': workouts})


def muscleGroups(request):
    user_info = request.session.get('user_info', None)
    muscle_groups = MuscleGroup.objects.all()
    return render(request, 'muscleGroups/muscleGroups.html', {'user_info': user_info, 'muscle_groups': muscle_groups})

def muscleGroup_workouts(request, pk):
    user_info = request.session.get('user_info', None)
    
    try:
        muscle_group_workout = MuscleGroupWorkout.objects.filter(id=pk)

    except MuscleGroupWorkout.DoesNotExist:
        muscle_group_workout = None
 

    return render(request, 'muscleGroups/muscleGroup_workouts.html', {'user_info': user_info,'muscle_group_workout': muscle_group_workout})
