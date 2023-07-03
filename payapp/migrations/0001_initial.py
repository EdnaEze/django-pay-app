# Generated by Django 4.2 on 2023-04-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('visit_date', models.DateField(verbose_name='visit date')),
                ('comment_str', models.CharField(max_length=500)),
            ],
        ),
    ]
