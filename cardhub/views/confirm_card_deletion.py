
from django.shortcuts import render
from django.views import View
from cardhub.models import UserCard

class ConfirmCardDeletion(View):

    def post(self, request):
        """ Buena práctica: delegar la lógica de consulta en un método privado"""
        user_card = self._query_user_card(request)
        
        """ Buena práctica: separar la lógica de construcción de la vista en un método privado"""
        template = 'confirm_card_deletion.html'
        built_view = self._build_confirm_card_deletion_view(request, user_card, template)
        return built_view

    def _query_user_card(self, request):
        """ Buena práctica: usar get para obtener valores del POST de forma segura"""
        card_id = request.POST.get('card_id')
        
        """ Buena práctica: manejar excepciones para evitar errores si no se encuentra el objeto"""
        try:
            user_card = UserCard.objects.get(_id=card_id)
        except UserCard.DoesNotExist:
            """Manejar la excepción de manera adecuada (podría redirigir a una página de error o mostrar un mensaje)"""
            user_card = None
        return user_card

    def _build_confirm_card_deletion_view(self, request, user_card, template):
        """ Buena práctica: utilizar render para devolver la respuesta con el contexto adecuado"""
        return render(request, template, {'card': user_card})
