from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.forms import ModelForm


class RegisterForm(forms.Form):
    username = forms.EmailField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')


class LoginForm(forms.Form):
    username = forms.CharField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')


class UpdateUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}), label='', required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
