from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency_choices = (
        ('GBP', 'GBP'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    currency = models.CharField(max_length=3, choices=currency_choices)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    @property
    def symbol(self):
        symbols = {
            'GBP': '£',
            'USD': '$',
            'EUR': '€',
        }
        return symbols.get(self.currency)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_payments', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.user.username} paid {self.amount} to {self.receiver.user.username}'
