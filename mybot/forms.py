from django import forms
from .models import SupportMessage

class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['message', 'image']

class SupportResponseForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['response']