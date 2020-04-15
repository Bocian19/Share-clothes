from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms import ModelForm
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import gettext as _
from .validators import check_password


class RegisterForm(forms.Form):
    username = forms.EmailField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(validators=[check_password], widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if len(password) < 8:
    #         raise forms.ValidationError(
    #             "Hasło powinno zawierać co najmniej 8 znaków")
    #     return password

    # def clean(self):
    #     cleaned_data = super(RegisterForm, self).clean()
    #     password = cleaned_data.get('password')
    #     if not password:
    #         raise forms.ValidationError('Hasłoooo powinno zawierać co najmniej 8 znaków')


class LoginForm(forms.Form):
    username = forms.CharField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')


class UpdateUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}), label='', required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
