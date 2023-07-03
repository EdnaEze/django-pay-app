from django.http import JsonResponse
from django.views import View
from .models import EXCHANGE_RATES
from django.http import HttpResponse

# Create your views here

class ConversionView(View):
    def get(self, request, currency1, currency2, amount_of_currency1):
        try:
            amount = float(amount_of_currency1)
            if currency1 not in EXCHANGE_RATES or currency2 not in EXCHANGE_RATES[currency1]:
                return JsonResponse({'error': 'Unsupported currency pair'}, status=400)
            rate = EXCHANGE_RATES[currency1][currency2]
            converted_amount = round(amount * rate, 2)
            return JsonResponse({'rate': rate, 'converted_amount': converted_amount})
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)


