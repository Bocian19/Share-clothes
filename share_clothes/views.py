from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from django.views import View
from share_clothes.models import Donation, Institution


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
        return render(request, 'register.html')