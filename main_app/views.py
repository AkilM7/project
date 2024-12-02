from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, PasswordResetForm
from django.contrib.auth.forms import PasswordResetForm
import logging

# Set up logger
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'main_app/newaccount.html', {'form': form})


# Login Page View
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.filter(email=email).first()
            if user:
                user = authenticate(request, username=user.username, password=password)
            
            if user:
                login(request, user)
                return redirect('home')  # Correct URL redirection
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'main_app/login.html', {'form': form})


# Forget Password View
def user_forgetpassword_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            request.session['user_id'] = user.id
            messages.success(request, 'Email verified. Proceed to reset password.')
            return redirect('resetpassword')
        else:
            messages.error(request, 'Email not found.')

    return render(request, 'main_app/forgetpassword.html')


# Reset Password View
def user_resetpassword_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    del request.session['user_id']  # Clear session after password reset
                    messages.success(request, 'Password reset successfully. Please log in.')
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Session expired. Please try again.')
    else:
        form = PasswordResetForm()

    return render(request, 'main_app/resetpassword.html', {'form': form})


# Home Page View
def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'main_app/home.html')  # Render the home page
    return redirect('login')


# Product Home View
def product_home_view(request):
    return render(request, 'main_app/producthome.html')


# Mobiles View
def mobiles_view(request):
    return render(request, 'main_app/mobiles.html')


# Profile View
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    context = {'user': user}  # Pass the user data to the template
    return render(request, 'main_app/profile.html', context)  # Render the profile page template


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

