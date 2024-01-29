import json

from cardhub.dao.CardHolderDao import CardHolderDao
from cardhub.dao.UserDao import UserDao
from cardhub.models import CardHolder, User
from django.http import JsonResponse


class ViewSignUp():
    
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.request = request
        self.error_message = "Invalid form submission method"
    
    
    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
        

    def _is_post_method(self):
        return self.request.method == "POST"
            

    def _build_response(self):
        newUser: User = UserDao().build_user(self.data)
        UserDao().save(newUser)
        card_holder = CardHolder(user=newUser)
        CardHolderDao().save(card_holder)
        response_data = {"signed": True}
        return JsonResponse([str(response_data["signed"])], safe=False)
