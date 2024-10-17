from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput

from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'date_of_birth']
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # User not active until email is verified
        user.is_active = False
        if commit:
            user.save()
        return user