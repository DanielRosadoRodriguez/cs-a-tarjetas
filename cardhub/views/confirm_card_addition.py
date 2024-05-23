
from django.shortcuts import render
from django.views import View
from cardhub.models import BankCard

class ConfirmCardAddition(View):
    """
    View for confirming the addition of a bank card.

    This class-based view handles POST requests to confirm the addition of a bank card
    by displaying a confirmation page with the selected card's details.

    Methods
    -------
    post(request)
        Handles POST requests to display the confirmation page for adding a bank card.
    """
    
    def post(self, request):
        """
        Handles POST requests to display the confirmation page for adding a bank card.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponse
            The rendered confirmation view with the selected bank card details.
        """
        bank_card = self._query_bank_card(request)
        template = 'confirm_card_addition.html'
        built_view = self._build_confirm_card_addition_view(request, bank_card, template)
        return built_view

    def _build_confirm_card_addition_view(self, request, bank_card, template):
        """
        Constructs the context for the confirmation view and renders the template.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.
        bank_card : BankCard
            The BankCard object containing the details of the selected card.
        template : str
            The name of the template to be rendered.

        Returns
        -------
        HttpResponse
            The rendered confirmation view with the context of the selected bank card.
        """
        return render(request, template, {'card': bank_card})

    def _query_bank_card(self, request):
        """
        Retrieves the BankCard object based on the provided card ID in the POST request.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        BankCard
            The BankCard object corresponding to the provided card ID.
        """
        card_id = request.POST.get('card_id')  
        bank_card = BankCard.objects.get(_id=card_id)
        return bank_card
