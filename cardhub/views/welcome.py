
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

class Welcome(View):
    
    def get(self, request):
        """ Buena práctica: utilizar un método privado para construir la vista de bienvenida"""
        welcome_view = self._build_welcome_view(request)
        return welcome_view

    def _build_welcome_view(self, request):
        """ Buena práctica: encapsular la lógica de construcción de la vista en un método privado"""
        welcome_view = render(request, 'welcome.html')
        return welcome_view

    def post(self, request):
        action = request.POST.get('action')
        """ Buena práctica: utilizar polimorfismo para manejar diferentes acciones en la solicitud POST"""
        if action == 'Log-In':
            return self._go_to_login_page()
        elif action == 'Sign-Up':
            return self._go_to_signup_page()
        else:
            """ Buena práctica: manejar acciones desconocidas de manera explícita"""
            return HttpResponse('Unknown action')
    
    def _go_to_login_page(self):
        """ Buena práctica: utilizar el método reverse para obtener la URL de la página de inicio de sesión"""
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_signup_page(self):
        """ Buena práctica: utilizar el método reverse para obtener la URL de la página de registro"""
        signup_url = reverse('signup')
        return redirect(signup_url)
