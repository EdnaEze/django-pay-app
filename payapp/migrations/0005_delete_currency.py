# Generated by Django 4.2 on 2023-05-03 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_paymentnotification_currency_user_profile_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
