from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.forms import UserForm
from cardhub.models import Cardholder, User
from django.contrib import messages
from django.db.utils import IntegrityError

class Signup(View):
    
    def get(self, request):
        sign_up_view = self._build_signup_view(request)
        return sign_up_view

    def _build_signup_view(self, request):
        sign_up_form = UserForm()
        sign_up_view = render(request, 'signup.html', {'form': sign_up_form})
        return sign_up_view

    def post(self, request):
        _register_user_response = self._register_user(request)
        return _register_user_response

    def _register_user(self, request):  
        form = UserForm(request.POST)
        if not form.is_valid(): return self._go_back_to_signup_page(request)
        new_user_data = form.cleaned_data
        try:
            self._save_user(new_user_data)
            self._send_success_message(request)
            return self._go_to_login_page()
        except IntegrityError as e:
            self._send_error_message(request)
            return self._go_back_to_signup_page(request)

    def _go_to_login_page(self):
        login_url = reverse('login')
        return redirect(login_url)

    def _send_success_message(self, request):
        success_message:str =  'User created successfully'
        messages.success(request, success_message)
    
    def _send_error_message(self, request):
        error_message = "This email is already in use. Please try again with a different email."
        messages.error(request, error_message)
                
        
    def _go_back_to_signup_page(self):
        signup_url = reverse('signup')
        return redirect(signup_url)
        
    def _save_user(self, data):
        cardholder = Cardholder.objects.create()
        user = User.objects.create(
            _name=data['name'],
            _email=data['email'],
            _password=data['password'],
            _cardholder=cardholder
        )
        return user
