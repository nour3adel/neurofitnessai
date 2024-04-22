from django.urls import path
from . import views

urlpatterns = [
    path("muscleGroups/", views.muscleGroups, name="muscleGroups"),
    path("muscleGroups/<str:name>/",views.muscleGroup_workouts,name="muscleGroups_workouts"),
    path("workout/<str:msw_name>/", views.workouts, name="workouts"),
    path("camera/<str:msw_name>/", views.camera, name="camera"),
    path("webcam_status/", views.webcam_status, name="webcam_status"),
    path("stop_camera/", views.stop_camera, name="stop_camera"),
    path("start_camera/", views.start_camera, name="start_camera"),
    path("webcam_feed/", views.webcam_feed, name="webcam_feed"),
]
