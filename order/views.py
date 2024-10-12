from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserConsultation
from .forms import UserConsultationForm

@login_required
def create_order(request):
    if request.method == 'POST':
        form = UserConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main-page')
    else:
        form = UserConsultationForm()
    return render(request, 'order/pages/CreateOrder.html', {'form': form})