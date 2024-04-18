from django.shortcuts import reverse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.forms import UserForm
from cardhub.models import Cardholder, User

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
            return self._go_to_login_page()
        except Exception as e:
            import traceback
            traceback.print_exc() 
        print(f"An error occurred")
        return self._go_back_to_signup_page(request)

    def _go_to_login_page(self):
        login_url = reverse('login')
        return redirect(login_url)

    def _go_back_to_signup_page(self, request):
        sign_up_page = render(request, 'signup.html', {'form': UserForm()})
        return sign_up_page
        
    def _save_user(self, data):
        print(f"Data: {data}")
        cardholder = Cardholder.objects.create()
        user = User.objects.create(
            _name=data['name'],
            _email=data['email'],
            _password=data['password'],
            _cardholder=cardholder
        )
        return user
