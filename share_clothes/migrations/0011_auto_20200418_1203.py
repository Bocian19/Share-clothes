# Generated by Django 3.0.4 on 2020-04-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_clothes', '0010_auto_20200413_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'verbose_name': 'Datek', 'verbose_name_plural': 'Datki'},
        ),
        migrations.AlterField(
            model_name='donation',
            name='address',
            field=models.CharField(max_length=64, verbose_name='Adres'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='city',
            field=models.CharField(max_length=36, verbose_name='Miasto'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=26, verbose_name='numer telefonu'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.CharField(max_length=64, null=True, verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(blank=True, default=None, verbose_name='Data odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_time',
            field=models.TimeField(blank=True, default=None, verbose_name='Godzina odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=20, verbose_name='Kod pocztowy'),
        ),
    ]