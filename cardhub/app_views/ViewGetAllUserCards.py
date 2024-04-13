
import json

from django.forms import model_to_dict

from ..models import CreditCardProduct
from ..models import CardHolderCard
from ..models import CardHolder

from django.http import JsonResponse


class GetAllUserCards():
        
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.email = self.data.get('email', '')


    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        card_holder = CardHolder.objects.get(user=self.email)
        card_holder_cards = CardHolderCard.objects.filter(card_holder=card_holder)
        cards = CreditCardProduct.objects.filter(cardholdercard__in=card_holder_cards)
        cards_data = [
            {
                'card_holder_card': model_to_dict(card_holder_card),
                'card': model_to_dict(card),
            }
            for card_holder_card, card in zip(card_holder_cards, cards)
        ]
        return JsonResponse(cards_data, safe=False)
