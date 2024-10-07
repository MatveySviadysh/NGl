from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Tutor

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TutorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Tutor
        fields = ['full_name', 'phone_number', 'specialization', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        
class TutorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                tutor = Tutor.objects.get(email=email)
                if not tutor.check_password(password):
                    raise forms.ValidationError("Неверный пароль")
            except Tutor.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден")
        return self.cleaned_data

    def get_Tutor(self):
        email = self.cleaned_data.get('email')
        return Tutor.objects.get(email=email)

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = None
        self.fields['new_password1'].label = None
        self.fields['new_password2'].label = None

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}))
