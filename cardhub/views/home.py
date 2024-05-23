from django.shortcuts import render
from django.views import View
from cardhub.models import User

class HomeView(View):

    def get(self, request):
        """ Buena práctica: usar un solo método para manejar tanto las solicitudes GET como las POST"""
        cardholder_view = self._build_home_view(request)
        return cardholder_view
    
    def post(self, request):
        """ Buena práctica: usar un solo método para manejar tanto las solicitudes GET como las POST"""
        cardholder_view = self._build_home_view(request)
        return cardholder_view
    
    def _build_home_view(self, request):
        """ Buena práctica: encapsular la lógica de construcción de la vista en un método privado"""
        username = self._query_user_name(request)
        cardholder = self._query_user(request).get_cardholder()
        cards = cardholder.get_all_cards()
        cardholder_view = render(request, 'home.html', {'username': username, 'cards': cards})
        return cardholder_view

    def _query_user_name(self, request):
        """ Buena práctica: encapsular la lógica de obtención del nombre de usuario en un método privado"""
        user = self._query_user(request)
        username = user.get_name()
        return username

    def _query_user(self, request):
        """ Buena práctica: encapsular la lógica de obtención del usuario en un método privado"""
        email = request.session['usr_email']
        user = User.objects.get(_email=email)
        return user
