from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard, CardStatement
from django.urls import reverse
from django.shortcuts import redirect, render
from cardhub.models import UserCard, WrongDateFormatException, BankCard
from datetime import date, datetime
from django.contrib import messages



class EditCard(View):
    """
    View for handling the editing of a user's card details.

    This class-based view handles POST requests to edit card details, add expenses, 
    add payments, and add statements. It also manages navigation to different pages 
    based on user actions.

    Methods
    -------
    post(request)
        Handles POST requests to manage different user actions such as cancel, save changes,
        add expenses, add payments, and add statements.
    
    date_to_str(input_date)
        Converts a date object to a string formatted as 'YYYY-MM-DD'.
    
    str_to_date(str_date)
        Converts a string formatted as 'YYYY-MM-DD' to a date object.
    
    edit(request, new_cut_off_date, new_payment_date)
        Helper method to edit and save the new cut-off and payment dates for the user's card.
        
    _send_error_message(request, error_message)
        Helper method to send an error message to the user.
    """
    
    def post(self, request):
        """
        Handles POST requests to manage different user actions such as cancel, save changes,
        add expenses, add payments, and add statements.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.

        Returns
        -------
        HttpResponseRedirect or HttpResponse
            A redirect response to the home or card details page, or the rendered edit card view.
        """
        # Check which button was pressed in the form
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'save_changes' in request.POST:
            card_id = request.POST['card_id']
            new_cut_off_date = request.POST.get('new_cut_off_date')
            new_payment_date = request.POST.get('new_payment_date')
            self.edit(request, new_cut_off_date, new_payment_date)
            return self._go_to_card_details(request)
        elif 'add_expenses' in request.POST:
            expenses = abs(float(request.POST.get('expenses')))
            self._add_expenses(request, expenses)
            return self._go_to_card_details(request)
        elif 'add_pay' in request.POST:
            pay = abs(float(request.POST.get('pay')))
            self._add_pay(request, pay)
            return self._go_to_card_details(request)
        elif 'add_statement' in request.POST:
            user_card = self._query_user_card(request)
            history = user_card.get_statement_history()
            owner_name = user_card.get_owner_name()
            current_date = datetime.now()
            debt = user_card.get_balance()
            interest = user_card.get_interest()
            
            statement = CardStatement.objects.create(
                _card=user_card,
                _owner_name=owner_name,
                _date=current_date,
                _payment_date=user_card.get_payment_date(),
                _cut_off_date=user_card.get_cut_off_date(),
                _debt=debt,
                _interest=interest
            )
            
            history.add_statement(statement=statement)
            
            cut_off_date = user_card.get_cut_off_date()
            payment_date = user_card.get_payment_date()
            
            new_cut_off_date = str(self._increment_month(cut_off_date))
            new_payment_date = str(self._increment_month(payment_date))
            
            user_card.set_payment_date(new_payment_date)
            user_card.set_cut_off_date(new_cut_off_date)
            user_card.save()
            
            return self._go_to_card_details(request)
        else:
            return self._build_response(request)

    def _increment_month(self, date_obj):
        """
        Increments the month of a given date, handling year transition if needed.

        Parameters
        ----------
        date_obj : date
            The date object whose month is to be incremented.

        Returns
        -------
        date
            The date object with the incremented month.
        """
        new_month = date_obj.month + 1
        new_year = date_obj.year
        # Add correct date for a new year
        if new_month > 12:
            new_month = 1
            new_year += 1
        return date_obj.replace(year=new_year, month=new_month)
 
    def _add_expenses(self, request, expenses):
        """
        Adds expenses to the user's card.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        expenses : float
            The amount of expenses to be added.
        """
        try:
            user_card = self._query_user_card(request)
            user_card.add_expense(expenses)
            user_card.save()
            self._send_success_message(request)
        except Exception as e:
            error_message = f"Error adding expenses: {str(e)}"
            self._send_error_message(request, error_message)
        
    def _add_pay(self, request, pay):
        """
        Adds a payment to the user's card.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        pay : float
            The amount of payment to be added.
        """
        try:
            user_card = self._query_user_card(request)
            user_card.pay(pay)
            user_card.save()
            self._send_success_message(request)
        except Exception as e:
            error_message = f"Error adding pay: {str(e)}"
            self._send_error_message(request, error_message)
            
    def _build_response(self, request):
        """
        Builds the response for rendering the edit card page.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered edit card view with the user's card details.
        """
        user_card = self._query_user_card(request)
        user_card_view = render(request, 'edit_card.html', {'user_card': user_card})
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
    
    def _go_to_card_details(self, request):
        """
        Redirects the user to the card details page.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the card details page.
        """
        request.session['card_id'] = request.POST['card_id']
        card_details_url = reverse('card_details')
        return redirect(card_details_url)
    
    def date_to_str(self, input_date):
        """
        Converts a date object to a string formatted as 'YYYY-MM-DD'.

        Parameters
        ----------
        input_date : date
            The date object to be converted.

        Returns
        -------
        str
            The formatted date string.

        Raises
        ------
        ValueError
            If the input date is empty or not a date object.
        """
        if not input_date:
            raise ValueError("Input date can't be empty")
        if not isinstance(input_date, date):
            raise ValueError("Cut off date must be a date")
        return input_date.strftime('%Y-%m-%d')

    def str_to_date(self, str_date):
        """
        Converts a string formatted as 'YYYY-MM-DD' to a date object.

        Parameters
        ----------
        str_date : str
            The date string to be converted.

        Returns
        -------
        date
            The converted date object.
        """
        return datetime.strptime(str_date, '%Y-%m-%d').date()

    def edit(self, request, new_cut_off_date, new_payment_date):
        """
        Edits and saves the new cut-off and payment dates for the user's card.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        new_cut_off_date : str
            The new cut-off date in string format.
        new_payment_date : str
            The new payment date in string format.

        Returns
        -------
        bool
            True if the changes are saved successfully, False otherwise.
        """
        try:
            user_card = self._query_user_card(request)
            user_card.set_payment_date(new_payment_date)
            user_card.set_cut_off_date(new_cut_off_date)
            user_card.save()
            self._send_success_message(request)
            return True
        except Exception as e:
            error_message = f"Error saving changes: {str(e)}"
            self._send_error_message(request, error_message)
            return False

    def _send_success_message(self, request):
        """
        Sends a success message to the user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        """
        success_message = 'Changes saved successfully'
        messages.success(request, success_message)
    
    def _send_error_message(self, request, error_message):
        """
        Sends an error message to the user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        error_message : str
            The error message to be sent.
        """
        messages.error(request, error_message)
