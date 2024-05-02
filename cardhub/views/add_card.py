from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from cardhub.models import BankCard, User, UserCard

class AddCardView(View):
    
    def get(self, request):
        add_card_view = self._build_add_card_view(request)
        return add_card_view
        
    def _build_add_card_view(self, request):
        available_cards = BankCard.objects.all()
        add_card_view = render(request, 'add_card.html', {'available_cards': available_cards})
        return add_card_view
    
    def post(self, request):
        card_id = request.POST['card_id']  
        bank_card = BankCard.objects.get(_id=card_id)
        user_card = UserCard.objects.create(
            _bank_card=bank_card,  
            _owner = self._query_user(request),  
            _payment_date=date.today(),  
            _cut_off_date=date.today() + timedelta(days=1),  
            _balance=0.0  
            )

        cardholder = self._query_user(request).get_cardholder()
        cardholder.add_card(user_card)
        return self._go_to_home_page()

    def _query_user(self, request):
        email = request.session['usr_email']
        user = User.objects.get(_email=email)
        return user

    def _go_to_home_page(self):
        home_url = reverse('home')
        return redirect(home_url)
