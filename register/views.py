from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from currency.models import EXCHANGE_RATES
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Payment
from django.contrib import messages


# Create your views here.
@csrf_protect
def register_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            # Create user account
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Create user profile with selected currency
            currency = request.POST.get('currency')
            if currency == 'GBP':
                initial_balance = 1000
            else:
                initial_balance = 1000 * EXCHANGE_RATES[currency]['GBP']
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.currency = currency
            user_profile.initial_balance = initial_balance
            user_profile.save()

            return redirect('home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            form = RegisterForm()
    return render(request, "register/register.html", {"register_user": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return render(request, "payapp/home.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    sent_payments = Payment.objects.filter(sender=user_profile)
    received_payments = Payment.objects.filter(receiver=user_profile)
    context = {'user_profile': user_profile, 'sent_payments': sent_payments, 'received_payments': received_payments}
    return render(request, 'register/dashboard.html', context)
