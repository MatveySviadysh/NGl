from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile-user')
    else:
        form = UserRegisterForm()
    return render(request, 'user/pages/registerUser.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile-user')
    else:
        form = UserLoginForm()
    return render(request, 'user/pages/loginUser.html', {'form': form})

def profile(request):
    return render(request, 'user/pages/profileUser.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('main-page')

def tutor_list(request, specialization):
    tutors = Tutor.objects.filter(specialization=specialization)
    return render(request, 'user/pages/TutorList.html', {'tutors': tutors, 'specialization': specialization})

def main_page(request):
    query = request.GET.get('query', '')
    if query:
        tutors = Tutor.objects.filter(specialization__icontains=query)
    else:
        tutors = Tutor.objects.all()

    specializations = Tutor.objects.values_list('specialization', flat=True).distinct()
    user_count = User.objects.count()
    popular_specializations = (Tutor.objects
        .values('specialization')
        .annotate(count=Count('id'))
        .order_by('-count')[:4])
    return render(request, 'user/pages/MainPage.html', {
        'specializations': specializations,
        'user_count': user_count,
        'popular_specializations': popular_specializations,
        'tutors': tutors,
        'query': query,
    })

def register_tutor(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            tutor = Tutor.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number'],
                specialization=form.cleaned_data['specialization'],
            )
            return redirect('profile-tutor')
    else:
        form = TutorRegistrationForm()
    return render(request, 'user/pages/RegisterTutor.html', {'form': form})

def login_tutor(request):
    if request.method == 'POST':
        form = TutorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                tutor = Tutor.objects.get(email=email)
                if tutor.check_password(password):
                    login(request, tutor)
                    messages.success(request, "Вы успешно вошли как репетитор!")
                    return redirect('profile-tutor')
                else:
                    messages.error(request, "Неверный пароль")
            except Tutor.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден")
    else:
        form = TutorLoginForm()
    return render(request, 'user/pages/LoginTutor.html', {'form': form})

def profile_tutor(request,id):
    tutor = get_object_or_404(Tutor, id=id)
    return render(request, 'user/pages/ProfileTutor.html', {'user': request.user}, {'tutor': tutor})

def tutor_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Вы успешно вышли из аккаунта!")
    return redirect('main-page')

def all_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'user/pages/AllTutors.html', {'tutors': tutors})

def notifications_user(request):
    return render(request, 'user/pages/NotificationsUser.html')

def change_password_user(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменён!')
            return redirect('profile-tutor')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/pages/ChangePassword.html', {'form': form})

def tutor_list_serarch(request):
    query = request.GET.get('query', '')
    tutors = Tutor.objects.filter(specialization__icontains=query) if query else []
    return render(request, 'user/pages/TutorsList.html', {
        'tutors': tutors,
        'query': query,
    })