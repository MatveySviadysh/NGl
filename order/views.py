from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    return render(request, 'order/pages/CreateOrder.html')
