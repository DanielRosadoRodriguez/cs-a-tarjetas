
from django.shortcuts import render
from django.views import View
from cardhub.models import User


class HomeView(View):
    """
    View for rendering the home page of the cardholder.

    This class-based view handles GET and POST requests to display the home page,
    which includes the cardholder's username and all their associated cards.

    Methods
    -------
    get(request)
        Handles GET requests to render the home page.
    
    post(request)
        Handles POST requests to render the home page.
    
    _build_home_view(request)
        Helper method to construct the context and render the home view.
    
    _query_user_name(request)
        Helper method to retrieve the username of the current user.
    
    _query_user(request)
        Helper method to retrieve the User object based on the session email.
    """
    
    def get(self, request):
        """
        Handles GET requests to render the home page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the GET request data.

        Returns
        -------
        HttpResponse
            The rendered home view with the username and cards.
        """
        cardholder_view = self._build_home_view(request)
        return cardholder_view
    
    def post(self, request):
        """
        Handles POST requests to render the home page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST request data.

        Returns
        -------
        HttpResponse
            The rendered home view with the username and cards.
        """
        cardholder_view = self._build_home_view(request)
        return cardholder_view
    
    def _build_home_view(self, request):
        """
        Constructs the context for the home view and renders the template.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered home view with the username and cards.
        """
        username = self._query_user_name(request)
        cardholder = self._query_user(request).get_cardholder()
        cards = cardholder.get_all_cards()
        cardholder_view = render(request, 'home.html', {'username': username, 'cards': cards})
        return cardholder_view

    def _query_user_name(self, request):
        """
        Retrieves the username of the current user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the session data.

        Returns
        -------
        str
            The username of the current user.
        """
        user = self._query_user(request)
        username = user.get_name()
        return username

    def _query_user(self, request):
        """
        Retrieves the User object based on the session email.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the session data.

        Returns
        -------
        User
            The User object corresponding to the session email.
        """
        email = request.session['usr_email']
        user = User.objects.get(_email=email)
        return user
