from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.forms import UserForm
from cardhub.models import Cardholder, User
from django.contrib import messages
from django.db.utils import IntegrityError

class Signup(View):
    
    def get(self, request):
        """ Buena práctica: utilizar un método privado para construir la vista de registro"""
        sign_up_view = self._build_signup_view(request)
        return sign_up_view

    def _build_signup_view(self, request):
        """ Buena práctica: encapsular la lógica de construcción de la vista en un método privado"""
        sign_up_form = UserForm()
        sign_up_view = render(request, 'signup.html', {'form': sign_up_form})
        return sign_up_view

    def post(self, request):
        """ Buena práctica: utilizar un método privado para manejar las solicitudes POST"""
        _register_user_response = self._register_user(request)
        return _register_user_response

    def _register_user(self, request):  
        form = UserForm(request.POST)
        if not form.is_valid(): return self._go_back_to_signup_page()
        new_user_data = form.cleaned_data
        if not self._is_new_email(request, new_user_data): return self._go_back_to_signup_page()
        
        try:
            self._save_user(new_user_data)
            self._send_success_message(request)
            return self._go_to_login_page()
        except IntegrityError as e:
            integrity_error_message = "Integrity Error, contact support"
            self._send_error_message(request, integrity_error_message)
            return self._go_back_to_signup_page()


    def _go_to_login_page(self):
        """ Buena práctica: utilizar el método reverse para obtener la URL de la página de inicio de sesión"""
        login_url = reverse('login')
        return redirect(login_url)

    def _is_new_email(self, request, new_user_data):
        given_email = new_user_data['email']
        if User.objects.filter(_email=given_email):
            error_message = "This email is already registered, please enter a new one."
            self._send_error_message(request, error_message=error_message)
            return False
        else:
            return True
        
    def _send_success_message(self, request):
        """ Buena práctica: enviar un mensaje de éxito después de que el usuario se registre exitosamente"""
        success_message = 'User created successfully'
        messages.success(request, success_message)
    
    def _send_error_message(self, request, error_message):
        """ Buena práctica: enviar un mensaje de error si ocurre un error durante el registro"""
        messages.error(request, error_message)
        
    def _go_back_to_signup_page(self):
        """ Buena práctica: redirigir de nuevo a la página de registro si hay un error durante el registro"""
        signup_url = reverse('signup')
        return redirect(signup_url)
        
    def _save_user(self, data):
        """ Buena práctica: separar la lógica para guardar un nuevo usuario en un método privado"""
        cardholder = Cardholder.objects.create()
        user = User.objects.create(
            _name=data['name'],
            _email=data['email'],
            _password=data['password'],
            _cardholder=cardholder
        )
        return user
