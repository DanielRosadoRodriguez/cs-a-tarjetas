from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard
from django.urls import reverse
from django.shortcuts import redirect, render
from cardhub.models import UserCard


class CardDetails(View):
    """
    View for displaying and managing details of a user's bank card.

    This class-based view handles GET and POST requests to display detailed
    information about a user's bank card, including statement history, and
    provides options to edit card information or cancel and return to the home
    page.

    Public Methods
    -------
    get(request)
        Handles GET requests to display the latest details of the user's bank card.
    
    post(request)
        Handles POST requests to process actions such as cancel, edit info, or display details.
   """
    
    def get(self, request):
        """
        Handles GET requests to display the updated values of the user's bank card.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered card details view with the user's card and statement history.
        """
        return self._show_updated_values(request)

    def post(self, request):
        """
        Handles POST requests to manage card details, including cancel, edit info, or display details.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponseRedirect or HttpResponse
            A redirect response to home or edit card page, or the rendered card details view.
        """
        
        # Check which button was clicked and redirect accordingly
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'edit_info' in request.POST:
            return self._go_to_edit() 
        else:
            return self._build_response(request)

    def _go_to_home_page(self):
        """
        Redirects the user to the home page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page.
        """
        home_url = reverse('home')
        return redirect(home_url)
    
    def _go_to_edit(self):
        """
        Redirects the user to the edit card page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the edit card page.
        """
        edit_card_url = reverse('edit_card')
        return redirect(edit_card_url)
    
    def _build_response(self, request):
        """
        Constructs the response for displaying card details and statement history.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered card details view with the user's card and statement history.
        """
        user_card = self._query_user_card(request)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view

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
        card_id = request.POST['card_id'] 
        user_card = UserCard.objects.get(_id=card_id)
        return user_card

    def _show_updated_values(self, request):
        """
        Retrieves and displays the updated values of the user's bank card.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered card details view with the user's card and statement history.
        """
        card_id = request.session['card_id']
        user_card = UserCard.objects.get(_id=card_id)
        statement_history = user_card.get_statement_history().get_all_statements()
        user_card_view = render(request, 'card_details.html', {'user_card': user_card, 'statement_history': statement_history})
        return user_card_view