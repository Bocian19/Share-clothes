from django.db import models

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

