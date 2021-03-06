from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.auth.password_validation import MinimumLengthValidator

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from share_clothes.models import Donation, Institution, Category
from share_clothes.forms import RegisterForm, LoginForm, UpdateUserForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json
from django.core.paginator import Paginator

from share_clothes.tokens import account_activation_token


class LandingPageView(View):

    def get(self, request):
        user1 = request.user
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        num_of_institutions_granted = Institution.objects.all().count()
        fundations_list = Institution.objects.all().filter(type='Fun')
        organisations_list = Institution.objects.all().filter(type='Org')
        collections_list = Institution.objects.all().filter(type='Zb')
        paginator = Paginator(fundations_list, 5)
        paginator1 = Paginator(organisations_list, 5)
        paginator2 = Paginator(collections_list, 5)

        page = 1
        fundations = paginator.get_page(page)
        organisations = paginator1.get_page(page)
        collections = paginator2.get_page(page)
        return render(request, 'index.html', {'quantity': quantity, "num_of_institutions": num_of_institutions_granted,
                                              "fundations": fundations, 'organisations': organisations,
                                              'collections': collections, 'user1': user1})

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            last_name = request.POST.get('surname')
            message = request.POST.get('message')
            current_site = get_current_site(request)
            mail_subject = 'Wiadomość od użytkonika poralu AddDOnation.'
            message = render_to_string('message.html', {
                'name': name,
                'last_name': last_name,
                'domain': current_site.domain,
                'message': message
            })
            admins = User.objects.all().filter(is_staff=True).filter(is_active=True)
            to_email = []
            for admin in admins:
                to_email.append(admin.email)
            email = EmailMessage(
                mail_subject, message, to=to_email
            )
            email.send()
            message = 'Wiadomość została wysłana.'
            return render(request, 'register.html', {'message': message})


def get_institution_for_pagination(request):
    data = request.GET.get('page')
    page_and_type = data.split(',')
    page = page_and_type[0]
    type_of_institution = page_and_type[1]
    institutions_list = Institution.objects.all().filter(type=type_of_institution)
    paginator = Paginator(institutions_list, 5)

    return render(request, 'updated_help.html', {'institutions': paginator.get_page(page), 'type': type_of_institution})


class AddDonationView(View):

    def get(self, request):
        user1 = request.user
        if user1.is_authenticated:
            return render(request, 'form.html', {"user1": user1, 'categories': Category.objects.all(),
                                                 'institutions': Institution.objects.all()})
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
            category_id = request.POST.get('categories')
            new_donation = Donation.objects.create(user_id=user1.id, quantity=quantity, address=address,
                                                   phone_number=phone_number, city=city,
                                                   zip_code=zip_code, pick_up_comment=pick_up_comment,
                                                   institution_id=institution_id,
                                                   pick_up_date=pick_up_date, pick_up_time=pick_up_time)

            if new_donation:
                new_donation.save()
                new_donation.categories.add(category_id)
                return render(request, 'form-confirmation.html', {'user1': user1})
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

    return render(request, 'form_summary.html',
                  {'category': category, 'institution': institution, 'bags': packages_quantity,
                   'adress': adress, 'city': city, 'code': code, 'phone': phone,
                   'date': date, 'time': time, 'more_info': more_info})


def get_update(request):
    user1 = request.user
    id = request.GET.get('id')
    print(id)
    updated_donation = Donation.objects.get(pk=id)
    updated_donation.is_taken = True
    updated_donation.save()
    if user1.is_authenticated:
        donations = Donation.objects.filter(user_id=user1.id)
        return render(request, 'user.html', {"user1": user1, 'donations': donations})
    return redirect('login')


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
        if request.method == 'POST':
            user1 = request.user
            if user1.is_authenticated:
                return render(request, 'form-confirmation.html', {'user1': user1})


class UserView(View):

    def get(self, request):
        user1 = request.user
        if user1.is_authenticated:
            donations = Donation.objects.filter(user_id=user1.id)
            return render(request, 'user.html', {"user1": user1, 'donations': donations})
        else:
            return redirect('login')

    def post(self, request):
        user1 = request.user
        f = UpdateUserForm(request.POST, instance=user1)
        if f.is_valid():
            pasword_new = request.POST.get('password')
            user1.set_password(pasword_new)
            f.save()
            user1.save()
            donations = Donation.objects.filter(user_id=user1.id)
            return render(request, "user.html", {'user1': user1, 'donations': donations})


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
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if user is not None:
                form.add_error('username', 'Użytkownik z tym adresem e-mail już jest zarejestrowany')
                return render(request, 'register.html', {'form': form})
            else:
                if confirm_password == password:
                    new_user = User.objects.create_user(username=username, email=username)
                    new_user.set_password(password)
                    new_user.is_active = False
                    new_user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Aktywacja konta na portalu AddDonation.'
                    message = render_to_string('activation_email.html', {
                        'user': new_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': account_activation_token.make_token(new_user),
                    })
                    to_email = form.cleaned_data.get('username')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    message = 'Wysłaliśmy na twój adres email link do atywacji konto.'
                    return render(request, 'register.html', {'message': message})
                else:
                    form.add_error('confirm_password', 'Powtórzone hasło jest inne niż pierwsze')
                    return render(request, 'register.html', {'form': form})
        else:
            form = RegisterForm(request.POST)
            return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        conf_info = "Dziękujemy za potwierdzenie konta użytkwnika"
        return render(request, 'index.html', {'user1': request.user, 'conf_info': conf_info})
    else:
        message = 'Link aktywacyjny stracił ważność'
        return render(request, 'register.html', {'message': message})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('homepage'))


class UpdateUserView(View):

    def get(self, request):
        user1 = request.user
        login_form = LoginForm(initial={'username': user1.username})
        info = 'Proszę najpierw o podanie hasła'
        return render(request, 'login.html', {'form': login_form, 'info': info, 'user1': user1})

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user1 = authenticate(username=username, password=password)
            if user1 is not None:
                form = UpdateUserForm(instance=user1)
                return render(request, "update_user_form.html", {"form": form, 'user1': user1})

            return redirect('login')
