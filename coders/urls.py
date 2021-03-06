"""coders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from share_clothes.views import LandingPageView, LoginView, AddDonationView, RegisterView, LogoutView, get_institution, \
    UserView, get_form_values, FormConfirmationView, get_update, UpdateUserView, get_institution_for_pagination,\
    activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='homepage'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('add-donation/', AddDonationView.as_view(), name='add-donation'),
    path('add-donations/', get_institution, name='update-form'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('summary/', get_form_values, name='summary'),
    path('form_confirmation/', FormConfirmationView.as_view, name='form-confirmation'),
    path('update-donation/', get_update, name='update-donation'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('update-pagination/', get_institution_for_pagination, name='update-pagination'),
    # url(r'^signup/$', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset', ),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
