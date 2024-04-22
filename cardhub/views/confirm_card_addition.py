
from django.shortcuts import render
from django.views import View
from cardhub.models import BankCard

class ConfirmCardAddition(View):

    def post(self, request):
        bank_card = self._query_bank_card(request)
        template = 'confirm_card_addition.html'
        built_view = self._build_confirm_card_addition_view(request, bank_card, template)
        return built_view

    def _build_confirm_card_addition_view(self, request, bank_card, template):
        return render(request, template, {'card': bank_card})

    def _query_bank_card(self, request):
        card_id = request.POST.get('card_id')  
        bank_card = BankCard.objects.get(_id=card_id)
        return bank_card
