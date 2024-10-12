from django import forms
from .models import UserConsultation

class UserConsultationForm(forms.ModelForm):
    class Meta:
        model = UserConsultation
        fields = '__all__'
