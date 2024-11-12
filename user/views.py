from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from store.models import Login
from .forms import RegistrationForm, LoginForm,ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This will handle saving the user with the hashed password
            messages.success(request, "Your account has been created successfully.")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            # If form is not valid, the errors will be shown in the template
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Login.objects.get(username=username)
                if check_password(password, user.password):
                    # Store user information in session
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['is_authenticated'] = True  # Custom session key to check authentication
                    return redirect('index')
                else:
                    form.add_error('password', 'Incorrect password')
            except Login.DoesNotExist:
                form.add_error('username', 'User does not exist')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    request.session.flush()  # Clear all session data
    return redirect('login')

def user_change_password(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    user = Login.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('index')
            else:
                form.add_error('old_password', 'Incorrect old password')
    else:
        form = ChangePasswordForm()

    return render(request, 'user/change_password.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Login.objects.filter(email=email).exists():
            otp = get_random_string(length=6, allowed_chars='1234567890')
            # Save OTP to user's profile or session, here using session for simplicity
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('validate_otp')
        else:
            messages.error(request, 'Email not found')
    return render(request, 'user/forgot_password.html')

def validate_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if otp == request.session.get('reset_otp'):
            if new_password == confirm_password:
                email = request.session.get('reset_email')
                user = Login.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'user/validate_otp.html')