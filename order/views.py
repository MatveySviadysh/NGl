from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from user.models import Tutor
from .models import UserConsultation
from .forms import UserConsultationForm

def answer(request):
    user_consultation = UserConsultation.objects.last()

    tutors = Tutor.objects.filter(
        specialization__icontains=user_consultation.specialization,
    )[:10]

    context = {
        'tutors': tutors,
        'user_consultation': user_consultation,
    }

    return render(request, 'order/pages/AnswerPage.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = UserConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('answer')
    else:
        form = UserConsultationForm()
    return render(request, 'order/pages/CreateOrder.html', {'form': form})