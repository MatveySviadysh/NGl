from django.shortcuts import render, redirect, get_object_or_404
from review.models import Comment
from chat.models import ChatRoom
from order.models import UserConsultation
from subscription.models import Subscription
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import random
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def chenge_user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-user')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user/pages/ChengeProfile.html', {'form': form, 'profile': profile})

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
    profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
    tutors = Tutor.objects.filter(specialization=specialization)
    tutor_count = tutors.count()
    paginator = Paginator(tutors, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/pages/TutorList.html', {
        'tutors': page_obj, 
        'specialization': specialization,
        'tutor_count': tutor_count,
        'page_obj': page_obj,  
        'profile': profile,
    })


def main_page(request):
    coutn_reviews = Review.objects.all().count()
    count_orders = UserConsultation.objects.all().count()
    if request.user.is_authenticated and hasattr(request.user, 'tutor'):
        tutor = request.user.tutor
    else:
        tutor = None
    profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
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
        'profile': profile, 
        'tutor':tutor,
        'count_orders':count_orders,
        'coutn_reviews': coutn_reviews,
    })

def register_tutor(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            tutor = Tutor.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number'],
                specialization=form.cleaned_data['specialization'],
                email=form.cleaned_data['email'],
            )
            return redirect('login_tutor')
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
                user = User.objects.get(email=email)
                tutor = Tutor.objects.get(user=user)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('main-page')
                else:
                    form.add_error(None, 'Неверный пароль')
            except User.DoesNotExist:
                form.add_error(None, 'Пользователь не найден.')
            except Tutor.DoesNotExist:
                form.add_error(None, 'Пользователь с таким email не найден.')
    else:
        form = TutorLoginForm()
    return render(request, 'user/pages/LoginTutor.html', {'form': form})

@login_required
def edit_tutor_profile(request):
    tutor = request.user.tutor
    if request.method == 'POST':
        form = TutorProfileUpdateForm(request.POST, request.FILES, instance=tutor)
        if form.is_valid():
            form.save()
            return redirect('main-page')
    else:
        form = TutorProfileUpdateForm(instance=tutor)
    return render(request, 'user/pages/EditTutorProfile.html', {'form': form})

def profile_tutor(request, full_name):
    tutor = Tutor.objects.filter(full_name=full_name).first()
    if tutor is None:
        print("Репетитор не найден для полного имени:", full_name)
        return render(request, 'user/pages/ProfileTutor.html', {'error': 'Репетитор не найден.'})
    profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
    is_subscribed = False
    chatroom = None
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, tutor=tutor).exists()
        if tutor.user is not None:
            chatroom, created = ChatRoom.objects.get_or_create(
                requester=request.user,
                responder=tutor.user,
                defaults={'chat_type': 'personal'}
            )
        else:
            print("Репетитор найден, но ассоциированный пользователь отсутствует.")

    comments = Comment.objects.filter(tutor=tutor).order_by('-created_at')
    comments_count = comments.count()
    star_range = range(1, 6)

    return render(request, 'user/pages/ProfileTutor.html', {
        'user': request.user,
        'tutor': tutor,
        'is_subscribed': is_subscribed,
        'profile': profile,
        'chatroom': chatroom,
        'comments': comments,
        'comments_count': comments_count,
        'star_range': star_range,
    })


def tutor_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Вы успешно вышли из аккаунта!")
        return redirect('main-page')
    return redirect('main-page')

def all_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'user/pages/AllTutors.html', {'tutors': tutors})


@login_required
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
    query = request.GET.get('query', '').strip()
    if query:
        tutors = Tutor.objects.filter(
            Q(specialization__icontains=query) | Q(full_name__icontains=query)
        )
    else:
        tutors = []
    return render(request, 'user/pages/TutorsList.html', {
        'tutors': tutors,
        'query': query,
    })

@login_required(login_url='login-user')
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.username = request.user.username
            review.save()
            return redirect('main-page')
    else:
        form = ReviewForm(user=request.user)
    return render(request, 'user/pages/review_form.html', {'form': form})

def all_review(request):
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 20)

    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)

    context = {
        'reviews': reviews,
        'star_range': range(1, 6)
    }
    
    return render(request, 'user/pages/AllReview.html', context)

def all_tutors(request):
    tutors = Tutor.objects.all()  
    paginator = Paginator(tutors, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'user/pages/AllTutors.html', {
        'tutors': page_obj,
        'tutor_count': tutors.count(),
        'page_obj': page_obj,
    })

def about_company(request):
    return render(request, 'user/pages/FotterPage/AboutCompany.html')

def all_service(request):
    all_specializations = Tutor.objects.values_list('specialization', flat=True).distinct()
    
    popular_specializations = (
        Tutor.objects
        .values('specialization')
        .annotate(count=Count('id'))
        .order_by('-count')[:4]
    )

    return render(request, 'user/pages/FotterPage/AllService.html', {
        'all_specializations': all_specializations,
        'popular_specializations': popular_specializations,
    })


def help_page(request):
    return render(request, 'user/pages/HelpPage.html')

def foregin_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(username=username) 
                user.set_password(new_password) 
                user.save()
                update_session_auth_hash(request, user)  
                return redirect('login-user')  
            except User.DoesNotExist:
                form.add_error('username', 'Пользователь не найден.')  
    else:
        form = PasswordResetForm()
    return render(request, 'user/pages/ForeginPassword.html', {'form': form})