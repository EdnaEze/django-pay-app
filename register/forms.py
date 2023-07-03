from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


CURRENCY_CHOICES = (
    ('USD', 'US dollars'),
    ('EUR', 'Euros'),
    ('GBP', 'GB Pounds'),
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "currency", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.currency = self.cleaned_data["currency"]
        user.save()
        return user


