from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard
from django.urls import reverse
from django.shortcuts import redirect, render
from cardhub.models import UserCard, WrongDateFormatException, BankCard
from datetime import date, datetime
from django.contrib import messages

class CardDetails(View):
    
    def get(self, request):
        return self._show_updated_values(request)

    def post(self, request):
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'edit_info' in request.POST:
            return self._go_to_edit() 
        else:
            return self._build_response(request)

    def _go_to_home_page(self):
        home_url = reverse('home')
        return redirect(home_url)
    
    def _go_to_edit(self):
        edit_card_url = reverse('edit_card')
        return redirect(edit_card_url)
    
    def _build_response(self, request):
        user_card = self._query_user_card(request)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view

    def _query_user_card(self, request):
        card_id = request.POST['card_id'] 
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _show_updated_values(self, request):
        card_id = request.session['card_id']
        user_card = UserCard.objects.get(_id=card_id)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view
