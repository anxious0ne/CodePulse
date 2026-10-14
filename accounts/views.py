from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from users.services import sync_user_codeforces

User = get_user_model()


def register_view(request):
    """Handles new user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        codeforces_handle = request.POST.get('codeforces_handle', '').strip() or None

        errors = []

        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('A user with that username already exists.')

        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        if codeforces_handle and User.objects.filter(codeforces_handle=codeforces_handle).exists():
            errors.append('That Codeforces handle is already registered with another account.')

        if errors:
            return render(request, 'accounts/register.html', {
                'errors': errors,
                'username': username,
                'email': email,
                'codeforces_handle': codeforces_handle or '',
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            codeforces_handle=codeforces_handle,
        )

        # Log in the user immediately
        auth_login(request, user)

        # Attempt initial sync if handle provided
        if codeforces_handle:
            try:
                sync_user_codeforces(user, codeforces_handle)
            except Exception:
                pass

        messages.success(request, f'Welcome to CodePulse, {username}!')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Handles user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password. Please try again.',
                'username': username,
                'next': next_url,
            })

    return render(request, 'accounts/login.html', {'next': next_url})


def logout_view(request):
    """Logs out the user and redirects to login."""
    auth_logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login-direct')
