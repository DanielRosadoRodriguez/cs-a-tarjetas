import json

from ..dao.AccountStatementDao import AccountStatementDao
from django.http import JsonResponse


class GetLastStatement():
        
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.cardholder_card_id = self.data['cardholder_card_id']


    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        return AccountStatementDao().get_last_card_statement(self.cardholder_card_id)
