from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from accounts.models import Profile
from .forms import UserRegistrationForm, UserLoginForm
from .models import OTP
import random
import string




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
    user = User.objects.get(id=user_id)
    otp = OTP.objects.get(user=user)
    otp_age = timezone.now() - otp.created_at
    
    remaining_time = 300 - int(otp_age.total_seconds())
    if request.method == 'POST':
        otp_list = request.POST.getlist('otp')
        otp_code = ''.join(otp_list)

        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_otp.html', {'error': 'OTP has expired.','remaining_time': max(0, remaining_time),'user': user})
            else:
                user.is_active = True
                user.save()
                otp.delete()
                login(request, user)
                return redirect('login')
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_otp.html', {'error': 'Invalid OTP.','remaining_time': max(0, remaining_time),'user': user})

    return render(request, 'auth/verify_otp.html', {'remaining_time': max(0, remaining_time),'user': user})


def verify_reset_otp(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp_list = request.POST.getlist('otp[]')
        otp_code = ''.join(otp_list)
        
        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_otp.html', {'error': 'OTP has expired.'})
            else:
                return redirect('password_reset', otp=otp.code)
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_reset_otp.html', {'error': 'Invalid OTP.'})
        
    return render(request, 'auth/verify_reset_otp.html',{'user':user})


def verify_two_step_otp(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp_list = request.POST.getlist('otp[]')
        otp_code = int(''.join(otp_list))
       
        try:
            otp = OTP.objects.get(user=user, code=otp_code)
            if otp.is_expired():
                return render(request, 'auth/verify_two_step_otp.html', {'error': 'OTP has expired.'})
            else:
                login(request, user)
                return redirect('home')
        except OTP.DoesNotExist:
            return render(request, 'auth/verify_two_step_otp.html', {'error': 'Invalid OTP.'})
        
    return render(request, 'auth/verify_two_step_otp.html', {'user':user})


def resend_otp(request, user_id):
    user = User.objects.get(id=user_id)
    otp = OTP.objects.filter(user=user)
    otp.delete()
    send_otp_to_user(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    

def User_Registration(request):
    if request.method == 'POST':
        username= f'{request.POST.get('first_name')}{request.POST.get('last_name')}{ ''.join(random.choices(string.digits, k=3))}'
        
        form_data ={
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'email': request.POST.get('email'),
        'username': username,
        'password1': request.POST.get('password1'),
        'password2': request.POST.get('password2'),
    }
        
        if (user := User.objects.filter(email=form_data['email']).first()) and user.is_active:
            return render(request, 'auth/registration_form.html',{'error':'Email already exists'})
        if form_data['password1'] != form_data['password2']:
            return render(request, 'auth/registration_form.html',{'error':'Passwords do not match'})
        
        form = UserRegistrationForm(form_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_otp_to_user(user)
            return redirect('verify_otp', user_id=user.id)
        else:
            print(form.errors,'this is erorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            return render(request, 'auth/registration_form.html',{'error':form.errors})
            
    else:
        form = UserRegistrationForm()
            
    return render(request, 'auth/registration_form.html')


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
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/login_form.html', {'form':form})


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
    