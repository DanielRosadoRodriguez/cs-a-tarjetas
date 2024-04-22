
from django.shortcuts import render
from django.views import View
from cardhub.models import UserCard

class ConfirmCardDeletion(View):

    def post(self, request):
        user_card = self._query_user_card(request)
        template = 'confirm_card_deletion.html'
        built_view = self._build_confirm_card_deletion_view(request, user_card, template)
        return built_view

    def _query_user_card(self, request):
        card_id = request.POST.get('card_id')  
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _build_confirm_card_deletion_view(self, request, user_card, template):
        return render(request, template, {'card': user_card})
