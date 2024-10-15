from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tutor, Subscription
from .forms import SubscriptionForm


@login_required(login_url='login-user')
def subscribe(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, tutor=tutor)
    
    if created:
        return redirect('profile-tutor',tutor.full_name)
    else:
        return redirect('profile-user')

@login_required(login_url='login-user')
def unsubscribe(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    Subscription.objects.filter(user=request.user, tutor=tutor).delete()
    return redirect('profile-tutor',tutor.full_name)