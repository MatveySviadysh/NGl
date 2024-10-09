from django.views import View
from django.shortcuts import render, redirect
from .forms import SupportMessageForm
from .models import SupportMessage
from django.contrib.auth.models import AnonymousUser

class ButtonPageView(View):
    def get(self, request, *args, **kwargs):
        form = SupportMessageForm()
        return render(request, 'mybot/button.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('login-user')  # Перенаправить на страницу входа, если пользователь не авторизован

        form = SupportMessageForm(request.POST)
        if form.is_valid():
            support_message = SupportMessage(
                name=request.user.username,
                email=request.user.email,
                message=form.cleaned_data['message'],
            )
            support_message.save()
            return redirect('main-page')
        else:
            print(form.errors)
        return render(request, 'mybot/button.html', {'form': form})
