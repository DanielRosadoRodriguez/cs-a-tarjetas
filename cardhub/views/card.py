from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from cardhub.models import UserCard
from django.urls import reverse
from django.shortcuts import redirect, render
from cardhub.models import UserCard, WrongDateFormatException



class Card(View):


    def post(self, request):
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'edit_payment_date' in request.POST:
            return self._edit_payment_date(request)
        elif 'edit_cut_off_date' in request.POST:
            return self._edit_cut_off_date(request)
        else:
            return self._build_response(request)

    def _build_response(self, request):
        user_card_view = render(request, 'user_card.html')
        return user_card_view

    def _go_to_home_page(self):
        home_url = reverse('home')
        return redirect(home_url)
    
    def _edit_payment_date(self, request):
        user_card = self._query_user_card(request)
        new_payment_date = request.POST.get('new_payment_date')
        try:
            user_card.set_payment_date(new_payment_date)
            user_card.save()
        except (ValueError, WrongDateFormatException) as e:
            return JsonResponse({'error': str(e)})
        return self._build_response(request)

    def _edit_cut_off_date(self, request):
        user_card = self._query_user_card(request)
        new_cut_off_date = request.POST.get('new_cut_off_date')
        try:
            user_card.set_cut_off_date(new_cut_off_date)
            user_card.save()
        except (ValueError, WrongDateFormatException) as e:
            return JsonResponse({'error': str(e)})
        return self._build_response(request)
    
    def _query_user_card(self, request):
        card_id = request.POST.get('card_id')  
        user_card = UserCard.objects.get(_id=card_id)
        return user_card
    