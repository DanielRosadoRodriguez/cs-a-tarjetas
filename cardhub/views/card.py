from django.views import View
from django.http import JsonResponse
from cardhub.models import UserCard

class Card(View):

    def post(self, request):
        user_card = self._query_user_card(request)
        card_information = JsonResponse(user_card.to_dict())  
        return card_information

    def _query_user_card(self, request):
        card_id = request.POST.get('card_id')  
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

