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
import random

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

def profile_user(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-user')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user/pages/profileUser.html', {'form': form, 'profile': profile})

def user_logout(request):
    logout(request)
    return redirect('main-page')

def tutor_list(request, specialization):
    tutors = Tutor.objects.filter(specialization=specialization)
    tutor_count = tutors.count()  
    return render(request, 'user/pages/TutorList.html', {
        'tutors': tutors, 
        'specialization': specialization,
        'tutor_count': tutor_count 
    })


def main_page(request):
    query = request.GET.get('query', '')
    if query:
         tutors = Tutor.objects.filter(specialization__icontains=query)
    else:
        tutors = Tutor.objects.all()

    all_reviews = list(Review.objects.all())
    random_reviews = random.sample(all_reviews, min(6, len(all_reviews)))
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
        'random_reviews':random_reviews,
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
            return redirect('profile-tutor', full_name=tutor.full_name)
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
                    return redirect('profile-tutor', full_name=tutor.full_name)
                else:
                    messages.error(request, "Неверный пароль")
            except Tutor.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден")
    else:
        form = TutorLoginForm()
    return render(request, 'user/pages/LoginTutor.html', {'form': form})

def profile_tutor(request, full_name):
    tutor = Tutor.objects.filter(full_name=full_name).first()
    if not tutor:
        return render(request, 'user/pages/404.html', status=404)
    return render(request, 'user/pages/ProfileTutor.html', {'user': request.user, 'tutor': tutor})

def tutor_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Вы успешно вышли из аккаунта!")
        return redirect('main-page')
    return redirect('main-page')

def all_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'user/pages/AllTutors.html', {'tutors': tutors})

def notifications_user(request):
    return render(request, 'user/pages/NotificationsUser.html')

def change_password_user(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменён!')
            return redirect('profile-user')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/pages/ChangePassword.html', {'form': form})

def tutor_list_serarch(request):
    query = request.GET.get('query', '')
    tutors = Tutor.objects.filter(specialization__icontains=query) if query else []
    return render(request, 'user/pages/TutorsList.html', {
        'tutors': tutors,
        'query': query,
    })

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.username = request.user.username
            review.save()
            return redirect('main-page')
        else:
            print(form.errors)
    else:
        form = ReviewForm(user=request.user)
    return render(request, 'review_form.html', {'form': form})
