# Generated by Django 4.2 on 2023-05-03 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payapp', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payapp.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='currency',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='currencies', to='register.userprofile'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
