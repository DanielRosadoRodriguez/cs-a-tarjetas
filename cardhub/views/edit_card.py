from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard
from django.urls import reverse
from django.contrib import messages
from datetime import date, datetime

class EditCard(View):

    def post(self, request):
        """ Buena práctica: utilizar estructuras condicionales claras para manejar diferentes acciones"""
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'save_changes' in request.POST:
            card_id = request.POST['card_id']
            new_cut_off_date = request.POST.get('new_cut_off_date')
            new_payment_date = request.POST.get('new_payment_date')
            self.edit(request, new_cut_off_date, new_payment_date)
            return self._go_to_card_details(request)
        else:
            return self._build_response(request)

    def _build_response(self, request):
        """ Buena práctica: encapsular la lógica de construcción de la respuesta en un método privado"""
        user_card = self._query_user_card(request)
        user_card_view = render(request, 'edit_card.html', {'user_card': user_card})
        return user_card_view

    def _query_user_card(self, request):
        """ Buena práctica: utilizar get para obtener valores del POST de forma segura"""
        card_id = request.POST['card_id']
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _go_to_home_page(self):
        """ Buena práctica: utilizar reverse para generar URLs dinámicamente y redirect para redirigir"""
        home_url = reverse('home')
        return redirect(home_url)

    def _go_to_card_details(self, request):
        """ Buena práctica: utilizar reverse para generar URLs dinámicamente y redirect para redirigir"""
        request.session['card_id'] = request.POST['card_id']
        card_details_url = reverse('card_details')
        return redirect(card_details_url)

    def date_to_str(self, input_date):
        """ Buena práctica: incluir comentarios que expliquen la función del método y cómo se debe utilizar
         Buena práctica: validar los parámetros de entrada y manejar excepciones si es necesario"""
        if not input_date: raise ValueError("Input date can't be empty")
        if not isinstance(input_date, date): raise ValueError("Cut off date must be a date")
        return input_date.strftime('%Y-%m-%d')

    def str_to_date(self, str_date):
        """ Buena práctica: incluir comentarios que expliquen la función del método y cómo se debe utilizar"""
        return datetime.strptime(str_date, '%Y-%m-%d').date()

    def edit (self, request, new_cut_off_date, new_payment_date):
        try:
            """ Buena práctica: utilizar try-except para manejar errores de forma controlada"""
            user_card = self._query_user_card(request)
            user_card.set_payment_date(new_payment_date)
            user_card.set_cut_off_date(new_cut_off_date)
            user_card.save()
            self._send_success_message(request)
            return True
        except Exception as e:
            """ Buena práctica: capturar excepciones específicas para manejar diferentes tipos de errores"""
            error_message = f"Error saving changes: {str(e)}"
            self._send_error_message(request, error_message)
            return False

    def _send_success_message(self, request):
        """ Buena práctica: utilizar mensajes flash para proporcionar retroalimentación al usuario"""
        success_message = 'Changes saved successfully'
        messages.success(request, success_message)
    
    def _send_error_message(self, request, error_message):
        """ Buena práctica: utilizar mensajes flash para proporcionar retroalimentación al usuario"""
        messages.error(request, error_message)
        