# Generated by Django 4.2 on 2023-05-04 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0007_payment_is_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='timestamp',
            new_name='date',
        ),
    ]
