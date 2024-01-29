
import json

from ..models import CardHolderCard

from ..dao.AccountStatementDao import AccountStatementDao
from django.http import JsonResponse


class ViewModifyStatement():
        
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.statement_id = self.data['statement_id']
        self.params = self._build_params()


    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
       original_statement = self._get_original_statement()
       new_statement = self._get_updated_statement(original_statement=original_statement)
       return new_statement


    def _get_original_statement(self):
        return AccountStatementDao().get(self.statement_id)
    
    
    def _get_updated_statement(self, original_statement):
        return AccountStatementDao().update(original_statement, self.params)
        

    def _build_params(self) -> dict:
        return {
            "date": self.data['date'],
            "cut_off_date" : self.data['cut_off_date'],
            "payment_date" : self.data['payment_date'],
            "current_debt" : self.data['current_debt'],
            "pni" : self.data['payment_for_no_interest'],
        }

