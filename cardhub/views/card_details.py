from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard
from django.urls import reverse
from cardhub.models import UserCard, WrongDateFormatException, BankCard
from datetime import date, datetime
from django.contrib import messages

class CardDetails(View):
    
    def get(self, request):
        """ Buena práctica: separar la lógica de presentación en métodos privados"""
        return self._show_updated_values(request)

    def post(self, request):
        """ Buena práctica: manejo claro de las diferentes acciones basadas en el POST request"""
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'edit_info' in request.POST:
            return self._go_to_edit() 
        else:
            return self._build_response(request)

    def _go_to_home_page(self):
        """ Buena práctica: utilizar reverse para generar URLs de manera dinámica y segura"""
        home_url = reverse('home')
        return redirect(home_url)
    
    def _go_to_edit(self):
        """ Buena práctica: utilizar reverse para la redirección a la vista de edición"""
        edit_card_url = reverse('edit_card')
        return redirect(edit_card_url)
    
    def _build_response(self, request):
        """ Buena práctica: encapsular la lógica de consulta y renderizado en métodos separados"""
        user_card = self._query_user_card(request)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view

    def _query_user_card(self, request):
        """ Buena práctica: separar la lógica de consulta a la base de datos en un método dedicado"""
        card_id = request.POST['card_id'] 
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _show_updated_values(self, request):
        """ Buena práctica: mantener la lógica de presentación separada de la lógica de negocio"""
        card_id = request.session['card_id']
        user_card = UserCard.objects.get(_id=card_id)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view

