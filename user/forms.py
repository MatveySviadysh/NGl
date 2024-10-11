from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Tutor, Review,UserProfile



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'avatar', 'description']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Почта'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class TutorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Tutor
        fields = [
            'full_name',
            'phone_number',
            'specialization',
            'email',
            'password',
            'password_confirm',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class TutorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = None
        self.fields['new_password1'].label = None
        self.fields['new_password2'].label = None

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.instance.username = self.user.username 

class TutorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['full_name', 'phone_number', 'specialization', 'email', 'avatar','price','services','video','experience',]