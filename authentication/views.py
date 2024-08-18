from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile
from .forms import UserRegistrationForm, UserLoginForm
from . models import OTP



def send_otp_to_user(user):
    otp, created = OTP.objects.get_or_create(user=user)
    if created:
        otp.save()

    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp.code}. It will expire in 5 minutes.',
        'noreply@example.com',
        [user.email],
        fail_silently=False,
    )

    return otp.code


def verify_otp(request, user_id):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        user = User.objects.get(id=user_id)

        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_otp.html', {'error': 'OTP has expired.'})
            else:
                otp.delete()
                login(request, user)
                return redirect('home')
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_otp.html', {'error': 'Invalid OTP.'})

    return render(request, 'auth/verify_otp.html', {'user_id': user_id})


def verify_reset_otp(request, user_id):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        user = User.objects.get(id=user_id)
        
        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_otp.html', {'error': 'OTP has expired.'})
            else:
                return redirect('password_reset', otp=otp.code)
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_reset_otp.html', {'error': 'Invalid OTP.'})
        
    return render(request, 'auth/verify_reset_otp.html')


def verify_two_step_otp(request, user_id):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        user = User.objects.get(id=user_id)
        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_two_step_otp.html', {'error': 'OTP has expired.'})
            else:
                login(request, user)
                return redirect('home')
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_two_step_otp.html', {'error': 'Invalid OTP.'})
        
    return render(request, 'auth/verify_two_step_otp.html', {})
    
    

def User_Registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_otp_to_user(user)
            return redirect('verify_otp', user_id=user.id)
    else:
        form = UserRegistrationForm()
            
    return render(request, 'auth/registration_form.html', {})


def User_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            profile = Profile.objects.get(user=user)
            if profile.two_step_auth:
                send_otp_to_user(user)
                return redirect('verify_two_step_otp', user_id=user.id)
            else:
                login(request, user)
                return redirect('home')
    return render(request, 'auth/login_form.html', {})


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_otp_to_user(user)
            return redirect('verify_reset_otp', user_id=user.id)
        except User.DoesNotExist:
            return render(request, 'password_reset_request.html', {'error': 'No account found with this email.'})
        
    return render(request, 'auth/password_reset_request.html', {})


def password_reset(request, otp_code):
    if request.method == 'POST':
        new_password = request.POST.get('password1')
        new_repert_password = request.POST.get('password2')
        if new_password == new_repert_password:
            try:
                otp = OTP.objects.get(code=otp_code)
                user = otp.user
                user.password = make_password(new_password)
                user.save()
                otp.delete()
                return redirect('login')
            except OTP.DoesNotExist:
                return render(request, 'auth/password_reset.html', {'error': 'Please try again later.'})
        else:
            return render(request, 'auth/password_reset.html',{'error': 'Password & Confirm Password do not match.'})
                
        
    return render(request, 'auth/password_reset.html')
    