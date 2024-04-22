from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('forget/', views.forget, name='forget'),
    path('user/', views.user, name='user'),  
    path('reset-code/', views.check_reset_otp, name='reset-code'),
    path('verify-code/', views.verify_otp, name='verify-code'),
    path('new-password/', views.new_password, name='new-password'),
    path('logout/', views.logout, name='logout'),
]
