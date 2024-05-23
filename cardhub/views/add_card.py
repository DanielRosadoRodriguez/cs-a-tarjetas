from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from cardhub.models import BankCard, User, UserCard

class AddCardView(View):

    def get(self, request):
        """ Buena práctica: mantener la lógica de la vista clara y separar responsabilidades"""
        add_card_view = self._build_add_card_view(request)
        return add_card_view
        
    def _build_add_card_view(self, request):
        """ Buena práctica: obtener todos los objetos de BankCard una vez y pasarlos al contexto de la vista"""
        available_cards = BankCard.objects.all()
        add_card_view = render(request, 'add_card.html', {'available_cards': available_cards})
        return add_card_view
    
    def post(self, request):
        """ Buena práctica: extraer datos del POST request"""
        """ Buena práctica: buscar el objeto requerido de manera eficiente"""
        card_id = request.POST['card_id']
        bank_card = BankCard.objects.get(_id=card_id) 
        
        """Buena práctica: utilizar create() para crear y guardar el objeto en una sola línea"""
        user_card = UserCard.objects.create(
            _bank_card=bank_card,  
            _owner=self._query_user(request),  
            _payment_date=date.today() + timedelta(days=1),  
            _cut_off_date=date.today(),  
            _balance=0.0  
        )

        cardholder = self._query_user(request).get_cardholder()
        cardholder.add_card(user_card)
        return self._go_to_home_page()

    def _query_user(self, request):
        """ Buena práctica: mantener las consultas a la base de datos encapsuladas en métodos separados"""
        email = request.session['usr_email']
        user = User.objects.get(_email=email)
        return user

    def _go_to_home_page(self):
        """ Buena práctica: utilizar reverse para generar URLs dinámicamente"""
        home_url = reverse('home')
        return redirect(home_url)
