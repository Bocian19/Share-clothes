# Generated by Django 3.0.4 on 2020-03-31 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_clothes', '0008_auto_20200331_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
