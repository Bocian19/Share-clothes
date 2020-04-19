from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64, null=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.name


class Institution(models.Model):
    FUNDACJA = 'Fun'
    ORGANIZACJA_POZARZADOWA = 'Org'
    ZBIORKA_LOKALNA = 'Zb'

    TYPE_CHOICES = [
        (FUNDACJA, "Fundacja"),
        (ORGANIZACJA_POZARZADOWA, "Organizacja pozarządowa"),
        (ZBIORKA_LOKALNA, "Zbiórka lokalna")]

    name = models.CharField(max_length=64, null=False, verbose_name="Nazwa")
    description = models.TextField(null=True, verbose_name="Opis")
    type = models.CharField(choices=TYPE_CHOICES, default=FUNDACJA, max_length=3, verbose_name="Typ organizacji")
    categories = models.ManyToManyField(Category, verbose_name="Kategoria")

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(null=False, max_length=64, verbose_name='Adres')
    phone_number = models.CharField(max_length=26, verbose_name='numer telefonu')
    city = models.CharField(max_length=36, verbose_name='Miasto')
    zip_code = models.CharField(max_length=20, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(auto_now=False,  auto_now_add=False, blank=True, default=None,
                                    verbose_name='Data odbioru')
    pick_up_time = models.TimeField(blank=True, default=None, verbose_name='Godzina odbioru')
    pick_up_comment = models.CharField(max_length=64, null=True, verbose_name='Komentarz')
    user = models.ForeignKey(User, blank=True, default=None, on_delete=models.CASCADE, null=True)
    is_taken = models.BooleanField(verbose_name='Dar odebrany', null=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

    class Meta:
        verbose_name = 'Datek'
        verbose_name_plural= 'Datki'

    def __str__(self):
        return self.institution.name



