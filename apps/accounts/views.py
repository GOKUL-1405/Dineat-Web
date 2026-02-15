from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import get_user_model


def login_view(request):
    """General login page - redirects to role-specific login"""
    return render(request, 'accounts/login.html')


def admin_login_view(request):
    """Admin login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_admin():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/admin-login.html')


def kitchen_login_view(request):
    """Kitchen staff login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_kitchen_staff():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:kitchen_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/kitchen-login.html')


def customer_login_view(request):
    """Customer login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_customer():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('orders:table_selection')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/customer-login.html')


@login_required
def logout_view(request):
    """Logout user and redirect to home"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('main:index')


def customer_signup_view(request):
    """Customer sign-up page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number', '')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/customer-signup.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'accounts/customer-signup.html')
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/customer-signup.html')
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'accounts/customer-signup.html')
        
        # Create new user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
                role='CUSTOMER'
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:customer_login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'accounts/customer-signup.html')
    
    return render(request, 'accounts/customer-signup.html')
