from django.shortcuts import render
from .models import MuscleGroup,Workout,MuscleGroupWorkout
from django.http import HttpResponse
from .camera import LiveWebCam
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.storage import staticfiles_storage
import logging


#region[Red] workouts 

def workouts(request, msw_name):
    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        try:
            muscle_group_workout = msw_name
            workout = Workout.objects.filter(musclegroup_workout=muscle_group_workout)
            
            equipment_labels = []
            protip = ''
            howto_sentences = []
            
            if workout.exists():
                workout_instance = workout[0]
                
                if workout_instance.howto:
                    howto_sentences = workout_instance.howto.split('//')
                
                if workout_instance.protip:
                    words = workout_instance.protip.split(' ')
                    protip = ' '.join(words)
                
                if workout_instance.equipments:
                    for item in workout_instance.equipments.split('.'):
                        parts = item.strip().split(':')
                        if len(parts) == 2:
                            equipment_labels.append((parts[0], parts[1]))
            else:
                workout_instance = None
            
        except Workout.DoesNotExist:
            workout_instance = None

        return render(request, 'muscleGroups/workoutss.html', {'user_info': user_info,
                                                              'workout_instance': workout_instance,
                                                              'equipment_labels': equipment_labels,
                                                              'protip': protip,
                                                              'howto_sentences': howto_sentences,
                                                              'muscle_group_workout':muscle_group_workout})
#endregion

#region[Blue] Muscle Groups 

def muscleGroups(request):
    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        muscle_groups = MuscleGroup.objects.all()
        return render(request, 'muscleGroups/muscleGroups.html', {'user_info': user_info, 'muscle_groups': muscle_groups})

#endregion

#region[white] Camera

# Instantiate LiveWebCam object outside of the view
live_cam_instance = LiveWebCam()
logger = logging.getLogger(__name__)
@csrf_exempt
def start_camera(request):
    try:
        if request.method == 'POST' and request.FILES.get('video_file'):
            video_file = request.FILES['video_file']
            
            success = live_cam_instance.start_capture(video_file)
            return JsonResponse({'success': success})
        else:
           
            success = live_cam_instance.start_capture()
            return JsonResponse({'success': success})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt
def stop_camera(request):
    try:   
        success = live_cam_instance.stop_capture()
        return JsonResponse({'success': success})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def webcam_status(request):
    if request.method == 'GET':
        try:
            success, stage, correct_reps, incorrect_reps ,feedback = live_cam_instance.get_camera_status()
            return JsonResponse({'status': success, 'stage': stage, 'correct_reps': correct_reps, 'incorrect_reps': incorrect_reps,'feedback': feedback})
        except Exception as e:
            logger.exception("Error getting webcam status")
            return JsonResponse({'status': False, 'stage': 'nan', 'correct_reps': 0, 'incorrect_reps': 0,'feedback': '',  'error': str(e)})

# Your existing gen and webcam_feed views remain unchanged
def gencam(camera,workout):
    for frame, landmarks in camera.get_frame(workout):
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@csrf_exempt       
def webcam_feed(request):
    workout  = request.GET.get('workout')
    print("--------------------------")
    print(workout)
    print("--------------------------")
    return StreamingHttpResponse(gencam(live_cam_instance,workout),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def camera(request, msw_name):
    user_info = request.session.get('user_info', None)
    if user_info is None:
        return render(request, 'pages/login_pages/login.html')
    else:
        muscle_group_workout = msw_name
        return render(request, 'muscleGroups/camera.html', {
            'user_info': user_info,
            'muscle_group_workout': muscle_group_workout
        })
#endregion

#region[Green] Muscle Groups Workouts
 
def muscleGroup_workouts(request, name):
    user_info = request.session.get('user_info')
    muscle_group_workout = None
    muscle_groups = name

    if user_info:
        try:
            muscle_group_workout = MuscleGroupWorkout.objects.filter(musclegroup=name)
            if not muscle_group_workout.exists():
                muscle_group_workout = None
                muscle_groups = name
        except MuscleGroupWorkout.DoesNotExist:
            muscle_group_workout = None
            muscle_groups = name

    return render(request, 'muscleGroups/muscleGroup_workouts.html', {
        'user_info': user_info,
        'muscle_group_workout': muscle_group_workout,
        'muscle_groups': muscle_groups,
    })
    
#endregion