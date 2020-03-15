from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from django.views import View
from share_clothes.models import Donation, Institution
from share_clothes.forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import redirect


class LandingPageView(View):

    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        num_of_institutions_granted = Institution.objects.all().count()
        institutions = Institution.objects.all()
        return render(request, 'index.html', {'quantity': quantity, "num_of_institutions": num_of_institutions_granted,
                                              "institutions": institutions})


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


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
                form.add_error('user', 'User already exist')
                return render(request, 'register.html', {'form': form})
            except:
                if confirm_password == password:
                    new_user = User.objects.create_user(username=username, password=password)
                    new_user.save()
                    return render(request, 'login.html')
                else:
                    form.add_error('confirm_password', 'Powtórzone hasło jest inne niż pierwsze')
                    return render(request, 'register.html', {'form': form})
        else:
            return render(request, 'register.html', {'form': form})

