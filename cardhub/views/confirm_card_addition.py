
from django.shortcuts import render
from django.views import View
from cardhub.models import BankCard

class ConfirmCardAddition(View):

    def post(self, request):
        """ Buena práctica: delegar la lógica de consulta en un método privado"""
        bank_card = self._query_bank_card(request)
        
        """ Buena práctica: separar la lógica de construcción de la vista en un método privado"""
        template = 'confirm_card_addition.html'
        built_view = self._build_confirm_card_addition_view(request, bank_card, template)
        return built_view

    def _build_confirm_card_addition_view(self, request, bank_card, template):
        """ Buena práctica: utilizar render para devolver la respuesta con el contexto adecuado"""
        return render(request, template, {'card': bank_card})

    def _query_bank_card(self, request):
        """ Buena práctica: usar get para obtener valores del POST de forma segura"""
        card_id = request.POST.get('card_id')
        
        """ Buena práctica: manejar excepciones para evitar errores si no se encuentra el objeto"""
        try:
            bank_card = BankCard.objects.get(_id=card_id)
        except BankCard.DoesNotExist:
            """ Manejar la excepción de manera adecuada (podría redirigir a una página de error o mostrar un mensaje)"""
            bank_card = None
        return bank_card

