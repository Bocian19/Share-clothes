# Generated by Django 3.0.4 on 2020-03-14 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_clothes', '0005_auto_20200314_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(to='share_clothes.Category'),
        ),
    ]
