from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='필수 항목입니다.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
