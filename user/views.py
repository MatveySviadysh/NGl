from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, '/user/pages/registerUser.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'user/pages/loginUser.html', {'form': form})

def profile(request):
    return render(request, 'user/pages/profileUser.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('login')
