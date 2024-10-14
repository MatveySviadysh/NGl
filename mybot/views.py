from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupportMessageForm, SupportResponseForm
from .models import SupportMessage
from django.contrib.auth.models import AnonymousUser


def Help_page(request):
    return render(request, 'mybot/HelpPage.html',)

class ButtonPageView(View):
    def get(self, request, *args, **kwargs):
        form = SupportMessageForm()
        return render(request, 'mybot/button.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('login-user')

        form = SupportMessageForm(request.POST, request.FILES)
        if form.is_valid():
            support_message = SupportMessage(
                name=request.user.username,
                email=request.user.email,
                message=form.cleaned_data['message'],
                image=request.FILES.get('image'),
            )
            support_message.save()
            return redirect('main-page')
        else:
            print(form.errors)
        return render(request, 'mybot/button.html', {'form': form})

class SupportMessageDetailView(View):
    def get(self, request, message_id):
        message = get_object_or_404(SupportMessage, id=message_id)
        response_form = SupportResponseForm(instance=message)
        return render(request, 'mybot/support_message_detail.html', {
            'message': message,
            'response_form': response_form,
        })
    
    def post(self, request, message_id):
        message = get_object_or_404(SupportMessage, id=message_id)
        response_form = SupportResponseForm(request.POST, instance=message)
        if response_form.is_valid():
            response_form.save()
            return redirect('admin:mybot_supportmessage_changelist')
        return render(request, 'mybot/support_message_detail.html', {
            'message': message,
            'response_form': response_form,
        })
    
class UserMessagesView(View):
    def get(self, request):
        messages = SupportMessage.objects.filter(name=request.user.username)
        return render(request, 'mybot/user_messages.html', {'messages': messages})
