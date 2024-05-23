from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from cardhub.models import UserCard

class DeleteCard(View):
    
    def post(self, request):
        self._remove_card_from_user_cardholder(request)
        self._delete_card_from_db(request)
        return self._go_to_home_page()
        
    def _remove_card_from_user_cardholder(self, request):
        card_to_remove = self._get_card_to_remove(request)
        owner = card_to_remove.get_owner()
        cardholder = owner.get_cardholder()
        cardholder.remove_card(card_to_remove)
 
    def _delete_card_from_db(self, request):
        card_to_remove = self._get_card_to_remove(request)
        card_to_remove.delete()
        
    def _get_card_to_remove(self, request):
        card_id = request.POST.get('card_id')  
        card_to_remove = UserCard.objects.get(_id=card_id)
        return card_to_remove

    def _go_to_home_page(self):
        cardholder_page = reverse('home')
        return redirect(cardholder_page)
    