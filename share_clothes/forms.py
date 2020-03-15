
from django import forms
from django.core.validators import EmailValidator


class RegisterForm(forms.Form):
    username = forms.EmailField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')


