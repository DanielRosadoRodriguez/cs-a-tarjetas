import json
from cardhub.domain.Authenticator import Authenticator
from django.http import JsonResponse


class ViewLogin():
    
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.email = self.data['email']
        self.password = self.data['password']
        self.error_message = "Invalid form submission method"
    
    
    def generate_json_response(self):
        if self._is_post_method():
            return self._build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        authenticator = Authenticator(self.email, self.password)
        is_authenticated = authenticator.authenticate_user()
        response_data = {"authenticated": str(is_authenticated)} 
        response_data_json = list(response_data.values())
        return JsonResponse(response_data_json, safe=False)
