from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from ..forms import CreateNewPerson
from ..models import User

class SignUp(View):
    
    def get(self, request):
        sign_up_view = self._build_signup_view(request)
        return sign_up_view
    

    def _build_signup_view(self, request):
        sign_up_form = CreateNewPerson()
        sign_up_view = render(request, 'add.html', {'form': sign_up_form})
        return sign_up_view


    def post(self, request):
        _register_user_response = self._register_user(request)
        return _register_user_response


    def _register_user(self, request):  
        form = CreateNewPerson(request.POST)
        if not form.is_valid(): self._go_back_to_signup_page(request)
        new_user_data = form.cleaned_data
        try:
            new_user = self._save_user(new_user_data)
            successful_signup_message = f"Person: { new_user.name } has been registered"
            successful_signup_notification = HttpResponse(successful_signup_message)
            return successful_signup_notification
        except Exception as e:
            print(f"An error occurred: {e}")
        self._go_back_to_signup_page(request)
        

    def _go_back_to_signup_page(self, request):
        sign_up_page = render(request, 'add.html', {'form': CreateNewPerson()})
        return sign_up_page
        
        
    def _save_user(self, data):
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
        )
        user.save()
        return user
