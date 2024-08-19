from django.urls import path
from . views import User_login, User_Registration, verify_otp, verify_reset_otp, verify_two_step_otp, password_reset_request, password_reset, resend_otp

urlpatterns = [
    path('login/', User_login, name='login'),
    path('registration/', User_Registration, name='registration '),
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp'),
    path('verify-reset-otp/<int:user_id>/', verify_reset_otp, name='verify_reset_otp'),
    path('verify-two-step-otp/<int:user_id>/', verify_two_step_otp, name='verify_two_step_otp'),
    path('password-reset-request/',password_reset_request, name='password_reset_request'),
    path('password-reset/<int:otp>/', password_reset, name='password_reset'),
    path('resend-otp/<int:user_id>/', resend_otp, name='resend_otp'),
]
