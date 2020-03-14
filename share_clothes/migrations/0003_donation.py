# Generated by Django 3.0.4 on 2020-03-14 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share_clothes', '0002_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Liczba worków')),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=26)),
                ('city', models.CharField(max_length=36)),
                ('zip_code', models.CharField(max_length=20)),
                ('pick_up_comment', models.CharField(max_length=64)),
                ('categories', models.ManyToManyField(to='share_clothes.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='share_clothes.Institution')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
