from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from cardhub.models import UserCard

class DeleteCard(View):
    """
    View for handling the deletion of a user's card.

    This class-based view handles POST requests to delete a user's card by removing it
    from the cardholder's list and deleting it from the database, then redirects to the home page.

    Methods
    -------
    post(request)
        Handles POST requests to delete the user's card and redirect to the home page.
    
    _remove_card_from_user_cardholder(request)
        Helper method to remove the card from the user's cardholder.
    
    _delete_card_from_db(request)
        Helper method to delete the card from the database.
    
    _get_card_to_remove(request)
        Helper method to retrieve the UserCard object based on the provided card ID.
    
    _go_to_home_page()
        Helper method to redirect the user to the home page.
    """
    
    def post(self, request):
        """
        Handles POST requests to delete the user's card and redirect to the home page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page after the card is deleted.
        """
        self._remove_card_from_user_cardholder(request)
        self._delete_card_from_db(request)
        return self._go_to_home_page()
        
    def _remove_card_from_user_cardholder(self, request):
        """
        Removes the card from the user's cardholder.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        """
        card_to_remove = self._get_card_to_remove(request)
        owner = card_to_remove.get_owner()
        cardholder = owner.get_cardholder()
        cardholder.remove_card(card_to_remove)
 
    def _delete_card_from_db(self, request):
        """
        Deletes the card from the database.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        """
        card_to_remove = self._get_card_to_remove(request)
        card_to_remove.delete()
        
    def _get_card_to_remove(self, request):
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
        card_to_remove = UserCard.objects.get(_id=card_id)
        return card_to_remove

    def _go_to_home_page(self):
        """
        Redirects the user to the home page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page.
        """
        cardholder_page = reverse('home')
        return redirect(cardholder_page)
