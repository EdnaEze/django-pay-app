from django.db import models
from django.contrib.auth.models import User
from register.models import UserProfile
from django.utils import timezone
# from django.contrib.auth.models import User


class Currency(models.Model):
    code = models.CharField(max_length=3, default='USD')
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=3)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='currencies', default=None)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.code


class Payment(models.Model):
    currency_choices = (
        ('GBP', 'GBP'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=currency_choices, default='USD')
    date = models.DateTimeField(auto_now_add=True)
    is_request = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.user.username} sent {self.amount} to {self.recipient.user.username}'


class PaymentNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.message}'
