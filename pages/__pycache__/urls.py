from django.urls import path
from . import views

urlpatterns = [
    
    path('muscleGroups/', views.muscleGroups, name='muscleGroups'),
    path('muscleGroups_workouts/<int:pk>/', views.muscleGroup_workouts, name='muscleGroups_workouts'),
    path('workouts/<int:pk>/', views.workouts, name='workouts'),
    
]