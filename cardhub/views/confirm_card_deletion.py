
from django.shortcuts import render
from django.views import View
from cardhub.models import UserCard

class ConfirmCardDeletion(View):
    """
    View for confirming the deletion of a user's card.

    This class-based view handles POST requests to confirm the deletion of a user's card
    by displaying a confirmation page with the selected card's details.

    Methods
    -------
    post(request)
        Handles POST requests to display the confirmation page for deleting a user's card.
    """
    
    def post(self, request):
        """
        Handles POST requests to display the confirmation page for deleting a user's card.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponse
            The rendered confirmation view with the selected user's card details.
        """
        user_card = self._query_user_card(request)
        template = 'confirm_card_deletion.html'
        built_view = self._build_confirm_card_deletion_view(request, user_card, template)
        return built_view

    def _query_user_card(self, request):
        """
        Retrieves the UserCard object based on the provided card ID in the POST request.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        UserCard
            The UserCard object corresponding to the provided card ID.
        """
        card_id = request.POST.get('card_id')  
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _build_confirm_card_deletion_view(self, request, user_card, template):
        """
        Constructs the context for the confirmation view and renders the template.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.
        user_card : UserCard
            The UserCard object containing the details of the selected card.
        template : str
            The name of the template to be rendered.

        Returns
        -------
        HttpResponse
            The rendered confirmation view with the context of the selected user's card.
        """
        return render(request, template, {'card': user_card})
