# Generated by Django 3.0.4 on 2020-04-18 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share_clothes', '0011_auto_20200418_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share_clothes.Institution'),
        ),
    ]
