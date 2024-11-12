from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.user_change_password, name='user_change_password'),
    path('passwordReset/', views.password_reset_request, name='forgot_password'),
    path('validate-otp/', views.validate_otp, name='validate_otp'),
]
