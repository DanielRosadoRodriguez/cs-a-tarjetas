import json

from ..dao.AccountStatementDao import AccountStatementDao
from ..models import CardHolderCard

from django.http import JsonResponse


class ViewGenerateCardStatement():
        
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.card_from_cardholder = CardHolderCard.objects.get(card_holder_cards_id=self.data['card_holder_cards_id'])
        self.params = self._build_params()


    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        statement = AccountStatementDao().build_card_statement(self.params)
        AccountStatementDao().save(statement)
        response_data = self._build_response_dict(statement)
        response = list([response_data])
        return JsonResponse(response, safe=False)
    
    
    def _build_params(self):
        return {
            'date': self.data['date'],
            'cut_off_date': self.data['cut_off_date'],
            'payment_date': self.data['payment_date'],
            'current_debt': self.data['current_debt'],
            'pni': self.data['pni'],
            'card_from_cardholder': self.card_from_cardholder
        }
    
    
    def _build_response_dict(self, statement):
        return {
            'statement_id': statement.statement_id,
            'date': statement.date,
            'cut_off_date': statement.cut_off_date,
            'payment_date': statement.payment_date,
            'current_debt': statement.current_debt,
            'payment_for_no_interest': statement.payment_for_no_interest,
            'card_from_cardholder': statement.card_from_cardholder.card_holder_cards_id
        }
        