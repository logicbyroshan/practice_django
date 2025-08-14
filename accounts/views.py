from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#User Model  : 1. username, first_name, last_name, email, password

# -------------------
# SIGNUP VIEW
# -------------------
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # 1. Passwords match?
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # 2. Username already taken?
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        # 4. Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'signup.html')


# -------------------
# LOGIN VIEW
# -------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# -------------------
# LOGOUT VIEW
# -------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------
# PROFILE VIEW
# -------------------
@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')
