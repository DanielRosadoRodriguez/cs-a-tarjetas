from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from cardhub.models import BankCard, User, UserCard, StatementHistory


class AddCardView(View):
    """
    View for handling the addition of a new bank card to a user's account.

    This class-based view handles GET and POST requests for the addition of a new
    bank card. The view renders a page displaying available bank cards for the
    user to select and handles the submission of the selected card, associating
    it with the user and initializing necessary details.

    Public Methods
    -------
    get(request)
        Handles GET requests to display available bank cards for selection.
    
    post(request)
        Handles POST requests to process the selection and add the card to the
        user's account.
    """
    
    def get(self, request):
        """
        Handles GET requests and renders the add card view with available bank cards.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered add card view with available bank cards.
        """
        add_card_view = self._build_add_card_view(request)
        return add_card_view
        
    def _build_add_card_view(self, request):
        """
        Constructs the context for the add card view and renders the template.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered add card view with the context of available bank cards.
        """
        available_cards = BankCard.objects.all()
        add_card_view = render(request, 'add_card.html', {'available_cards': available_cards})
        return add_card_view
    
    def post(self, request):
        """
        Handles POST requests to add a selected bank card to the user's account.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page after successfully adding the card.
        """
        card_id = request.POST['card_id']  
        bank_card = BankCard.objects.get(_id=card_id)
        statement_history = StatementHistory.objects.create()

        user_card = UserCard.objects.create(
            _bank_card=bank_card,  
            _owner = self._query_user(request),  
            _payment_date=date.today() + timedelta(days=1),  
            _cut_off_date=date.today(),  
            _balance=0.0,
            _statement_history=statement_history
            )

        cardholder = self._query_user(request).get_cardholder()
        cardholder.add_card(user_card)
        return self._go_to_home_page()

    def _query_user(self, request):
        """
        Retrieves the User object based on the email stored in the session.

        Parameters
        ----------
        request : HttpRequest
            The request object used to access session data.

        Returns
        -------
        User
            The User object corresponding to the email stored in the session.
        """
        email = request.session['usr_email']
        user = User.objects.get(_email=email)
        return user

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
