# Generated by Django 4.2 on 2023-05-03 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_userprofile_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]