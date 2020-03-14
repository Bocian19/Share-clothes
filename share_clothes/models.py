from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64, null=False)


class Institution(models.Model):
    FUNDACJA = 'Fun'
    ORGANIZACJA_POZARZADOWA = 'Org'
    ZBIORKA_LOKALNA = 'Zb'

    TYPE_CHOICES = [
        (FUNDACJA, "Fundacja"),
        (ORGANIZACJA_POZARZADOWA, "Organizacja pozarządowa"),
        (ZBIORKA_LOKALNA, "Zbiórka lokalna")]

    name = models.CharField(max_length=64, null=False)
    description = models.TextField(null=True)
    type = models.CharField(choices=TYPE_CHOICES, default=FUNDACJA, max_length=3)


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.CharField(null=False, max_length=64)
    phone_number = models.CharField(max_length=26)
    city = models.CharField(max_length=36)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField(auto_now=False,  auto_now_add=False, blank=True, default=None)
    pick_up_time = models.TimeField(blank=True, default=None)
    pick_up_comment = models.CharField(max_length=64)
    user = models.ForeignKey(User, blank=True, default=None, on_delete=models.PROTECT, null=True)











