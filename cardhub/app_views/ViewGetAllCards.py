from ..dao import CreditCardProductDao
from django.http import JsonResponse
from ..dao.CreditCardProductDao import CreditCardProductDao


class ViewGetAllCards():
    
    def generate_json_response(self):
        cards = CreditCardProductDao().get_all()
        cards_json = list(cards.values())
        return JsonResponse(cards_json, safe=False)
