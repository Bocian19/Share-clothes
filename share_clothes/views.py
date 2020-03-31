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
        user1 = request.user
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        num_of_institutions_granted = Institution.objects.all().count()
        institutions = Institution.objects.all()
        return render(request, 'index.html', {'quantity': quantity, "num_of_institutions": num_of_institutions_granted,
                                              "institutions": institutions, 'user1': user1})


class AddDonationView(View):

    def get(self, request):
        user1 = request.user
        if user1.is_authenticated:
            return render(request, 'form.html', {"user1": user1, 'categories': Category.objects.all(), 'institutions': Institution.objects.all()})
        else:
            return redirect('login')

    def post(self, request):
        if request.method == 'POST':
            user1 = request.user
            quantity = request.POST.get('bags')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            zip_code = request.POST.get('postcode')
            pick_up_comment = request.POST.get('more_info')
            institution_id = request.POST.get('organization')
            pick_up_date = request.POST.get('data')
            pick_up_time = request.POST.get('time')
            new_donation = Donation.objects.create(user_id=user1.id, quantity=quantity, address=address, phone_number=phone_number, city=city,
                                               zip_code=zip_code, pick_up_comment=pick_up_comment, institution_id=institution_id,
                                               pick_up_date=pick_up_date, pick_up_time=pick_up_time)
            if new_donation:
                new_donation.save()
                return render(request, 'form-confirmation.html')
            else:
                info = "Nie udało się zaipsać formularza"
                return render(request, 'form-confirmation.html', {'info': info})
        info = 'Coś poszło nie tak'
        return redirect(request, 'form-confirmation.html', {'info': info})


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
    friendly_data = json.loads(income_data)
    institution_id = friendly_data[3]['value']
    institution = Institution.objects.get(pk=institution_id)
    packages_quantity = friendly_data[2]['value']
    category = Category.objects.get(pk=friendly_data[1]['value'])
    adress = friendly_data[4]['value']
    city = friendly_data[5]['value']
    code = friendly_data[6]['value']
    phone = friendly_data[7]['value']
    date = friendly_data[8]['value']
    time = friendly_data[9]['value']
    more_info = friendly_data[10]['value']

    return render(request, 'form_summary.html', {'category': category, 'institution': institution, 'bags': packages_quantity,
                                                 'adress': adress, 'city': city, 'code': code, 'phone': phone,
                                                 'date': date, 'time': time, 'more_info': more_info })


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


class FormConfirmationView(View):

    def post(self, request):
        user1 = request.user
        return render(request, 'form-confirmation.html', {'user1': user1})


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


