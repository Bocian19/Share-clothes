from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from share_clothes.models import Donation, Institution, Category
from share_clothes.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json


class LandingPageView(View):

    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        num_of_institutions_granted = Institution.objects.all().count()
        institutions = Institution.objects.all()
        return render(request, 'index.html', {'quantity': quantity, "num_of_institutions": num_of_institutions_granted,
                                              "institutions": institutions})


class AddDonationView(View):

    def get(self, request):
        user1 = request.user
        if user1.is_authenticated:
            return render(request, 'form.html', {"user1": user1, 'categories': Category.objects.all(), 'institutions': Institution.objects.all()})
        else:
            return redirect('login')


def get_institution(request):
    cat_id = request.GET.get('cat_id')
    cats_id = cat_id.split(',')
    if len(cats_id) > 0:
        institutions = Institution.objects.filter(categories__in=Category.objects.filter(pk__in=cats_id))
    elif len(cats_id) == 0:
        institutions = Institution.objects.filter(categories__in=Category.objects.get(pk=cats_id[0]))
    else:
        institutions = Institution.objects.all()

    return render(request, 'updated_form.html', {'institutions': institutions})


def get_form_values(request):
    income_data = request.GET.get('data')
    print(type(income_data))
    institution_id = income_data[0]
    institution = Institution.objects.get(pk=institution_id)

    return render(request, 'form_summary.html', {'institution': institution})


class LoginView(View):

    def get(self, request):
        form = LoginForm
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logging_user = authenticate(username=user_login, password=password)
            if logging_user is not None:
                login(request, logging_user)
                return redirect(reverse_lazy('homepage'))
            else:
                response = "Brak użytkownia"
                return render(request, 'register.html', {'form': form, 'response': response})


class UserView(View):

    def get(self, request):
        user1 = request.user
        if user1.is_authenticated:
            return render(request, 'user.html', {"user1": user1})
        else:
            return redirect('login')


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            try:
                User.objects.get(username=username)
                form.add_error('user', 'Użytkownik z tym adresem e-mail już jest zarejestrowany')
                return render(request, 'register.html', {'form': form})
            except:
                if confirm_password == password:
                    new_user = User.objects.create_user(username=username, password=password)
                    new_user.save()
                    return redirect('login')
                else:
                    form.add_error('confirm_password', 'Powtórzone hasło jest inne niż pierwsze')
                    return render(request, 'register.html', {'form': form})
        else:
            return render(request, 'register.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('homepage'))


