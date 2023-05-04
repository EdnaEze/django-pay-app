from django import forms
from .models import Payment
from .models import PaymentNotification
from django.core.validators import MinValueValidator


class PaymentForm(forms.ModelForm):
    receiver_username = forms.CharField()
    amount = forms.DecimalField(validators=[MinValueValidator(0)])
    currency = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')])
    is_direct = forms.BooleanField(required=False)

    class Meta:
        model = Payment
        fields = ['receiver_username', 'amount', 'currency', 'is_direct']


class PaymentNotificationForm(forms.ModelForm):
    class Meta:
        model = PaymentNotification
        fields = ['user', 'payment', 'message']
