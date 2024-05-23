from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from cardhub.models import UserCard

class DeleteCard(View):
    
    def post(self, request):
        """ Buena práctica: separar la lógica de eliminación en un método privado"""
        self._remove_card_from_user_cardholder(request)
        
        """ Buena práctica: redirigir de manera clara y segura utilizando reverse y redirect"""
        return self._go_to_home_page()
        
    def _remove_card_from_user_cardholder(self, request):
        """ Buena práctica: encapsular la lógica de obtención y eliminación de la tarjeta en métodos separados"""
        card_to_remove = self._get_card_to_remove(request)
        owner = card_to_remove.get_owner()
        cardholder = owner.get_cardholder()
        cardholder.remove_card(card_to_remove)

    def _get_card_to_remove(self, request):
        """ Buena práctica: utilizar get para obtener valores del POST de forma segura"""
        card_id = request.POST.get('card_id')  
        card_to_remove = UserCard.objects.get(_id=card_id)
        return card_to_remove

    def _go_to_home_page(self):
        """ Buena práctica: utilizar reverse para generar URLs dinámicamente y redirect para redirigir"""
        cardholder_page = reverse('home')
        return redirect(cardholder_page)
    