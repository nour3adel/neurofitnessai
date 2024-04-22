from django.shortcuts import render
from .models import History
from muscleGroups.models import Workout


#region[Red] Dashboard
def dashboard(request):
    
    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        return render(request, 'customer/dashboard.html', {'user_info': user_info,'workoutss':Workout.objects.all()})

#endregion

#region[green] profile

def profile(request):
    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        return render(request, 'customer/profile.html', {'user_info': user_info,'workoutss':Workout.objects.all()})

#endregion

#region[Blue] History

def history(request):

    user_info = request.session.get('user_info', None)
    if user_info is None:
        # Handle the case when user is not logged in
        # For example, you can render a different template or return an error message
        return render(request, 'pages/login_pages/login.html')
    else:
        if user_info and 'id' in user_info:
            user_id = user_info['id']
            user_history = History.objects.filter(user_id=user_id)
        else:
            # Handle the case where the user is not logged in or the user ID is not present
            user_history = []

    return render(request, 'customer/history.html', {'user_info': user_info, 'history': user_history})

#endregion