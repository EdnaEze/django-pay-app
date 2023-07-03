from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import json
from currency.views import ConversionView
from register.models import UserProfile
from .forms import PaymentForm
from .models import Payment, PaymentNotification, Currency
from decimal import Decimal


def home(request):
    return render(request, 'payapp/home.html')


@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    currency_symbol = user_profile.symbol
    payments = Payment.objects.filter(Q(sender=user_profile) | Q(recipient=user_profile)).order_by('-date')
    context = {
        'user_profile': user_profile,
        'currency_symbol': currency_symbol,
        'payments': payments,
        'balance': user_profile.balance
    }
    return render(request, 'payapp/dashboard.html', context)


@csrf_protect
@login_required
def transfer(request):
    if request.method == 'POST':
        sender_profile = UserProfile.objects.get(user=request.user)
        receiver_username = request.POST.get('receiver_username')
        amount = Decimal(request.POST.get('amount'))
        currency = request.POST.get('currency')
        # is_direct = request.POST.get('is_direct') == 'True'

        try:
            receiver_profile = UserProfile.objects.get(user__username=receiver_username)
            print(f"Receiver profile found: {receiver_profile}")
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid receiver username')
            print(f"Receiver profile not found for username: {receiver_username}")
            return redirect('transfer')

        if sender_profile.balance < amount:
            print(sender_profile.balance)
            messages.error(request, 'Insufficient balance')
            return redirect('transfer')

        conversion_view = ConversionView()
        response = conversion_view.get(request, currency1=currency, currency2=sender_profile.currency, amount_of_currency1=amount)
        if isinstance(response, JsonResponse):
            response_dict = json.loads(response.content)
            if response_dict.get('error'):
                messages.error(request, response_dict['error'])
                return redirect('transfer')
            exchange_rate = response_dict['rate']
            amount_usd = Decimal(response_dict['converted_amount'])
        else:
            exchange_rate = response['rate']
            amount_usd = Decimal(response['converted_amount'])

        # update sender and receiver balance
        sender_profile.balance -= amount_usd
        receiver_amount = amount * Decimal(exchange_rate)
        receiver_profile.balance += receiver_amount

        # Save sender and receiver profiles
        sender_profile.save()
        receiver_profile.save()

        # Create payment object
        payment = Payment(sender=sender_profile, recipient=receiver_profile, amount=amount_usd, currency=currency)
        payment.save()

        # Create payment notification for recipient user
        receiver_notification = PaymentNotification(
            user=receiver_profile.user,
            payment=payment,
            message=f"You received a payment of {amount} {currency} from {sender_profile.user.username}"
        )
        receiver_notification.save()

        # Create payment notification for sender user
        sender_notification = PaymentNotification(
            user=sender_profile.user,
            payment=payment,
            message=f"You sent a payment of {amount} {currency} to {receiver_profile.user.username}"
        )
        sender_notification.save()

        messages.success(request, 'Payment successful')
        return redirect('dashboard')

    form = PaymentForm()
    context = {
        'form': form,
    }
    return render(request, 'payapp/transfer.html', context)


@csrf_protect
@login_required
def request_payment(request):
    if request.method == 'POST':
        sender_profile = UserProfile.objects.get(user=request.user)
        receiver_username = request.POST.get('receiver_username')
        amount = Decimal(request.POST.get('amount'))
        currency = request.POST.get('currency')

        try:
            receiver_profile = UserProfile.objects.get(user__username=receiver_username)
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid receiver username')
            return redirect('request_payment')

        # Check if the sender is not requesting payment from themselves
        if sender_profile == receiver_profile:
            messages.error(request, "You can't request payment from yourself")
            return redirect('request_payment')

        Payment.objects.create(sender=sender_profile, recipient=receiver_profile, currency=currency, amount=amount, is_request=True)
        messages.success(request, 'Payment request sent')
        return redirect('dashboard')
    return render(request, 'payapp/request.html')


# @csrf_protect
@login_required
def view_transactions(request):
    user = request.user
    payments = Payment.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-date')
    return render(request, 'payapp/dashboard.html', {'payment': payments})


@login_required
def admin_view(request):
    if not request.user.is_superuser:
        messages.error(request, f'You are not authorized to view this page')
        return redirect('home')
    users = User.objects.all()
    payment = Payment.objects.all()
    context = {
        'users': users,
        'transactions': payment,
    }
    return render(request, 'payapp/admin.html', context)
