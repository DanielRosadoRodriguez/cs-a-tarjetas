
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from cardhub.domain.authenticator import Authenticator
from cardhub.exceptions.EmailNotRegisteredException import EmailNotRegisteredException
from cardhub.exceptions.IncorrectPasswordException import IncorrectPasswordException
from cardhub.forms import LogInForm
from cardhub.models import User
from django.contrib import messages


class Login(View):
    """
    View for handling user login.

    This class-based view handles GET and POST requests for the login page.
    It renders the login form and processes user authentication.

    Methods
    -------
    get(request)
        Handles GET requests to render the login page.
    
    post(request)
        Handles POST requests to authenticate the user.
    """
    
    def get(self, request):
        """
        Handles GET requests to render the login page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the GET request data.

        Returns
        -------
        HttpResponse
            The rendered login view with an empty login form.
        """
        log_in_view = self._build_log_in_view(request)
        return log_in_view

    def post(self, request):
        """
        Handles POST requests to authenticate the user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST request data.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the appropriate page based on the login result.
        """
        _log_in_user_response = self._log_in_user(request)
        return _log_in_user_response

    def _build_log_in_view(self, request):
        """
        Constructs the login view with an empty login form.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered login view with an empty login form.
        """
        log_in_form = LogInForm()
        log_in_view = render(request, 'login.html', {'form': log_in_form})
        return log_in_view

    def _log_in_user(self, request):
        """
        Authenticates the user based on the submitted login form.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST data with the login form.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page if login is successful,
            or back to the login page if login fails.
        """
        form = LogInForm(request.POST)
        if not form.is_valid():
            return self._go_back_to_log_in_page()
        
        user_data = form.cleaned_data
        try:
            # Attempt to authenticate the user
            authenticated_user = Authenticator(
                users=list(User.objects.all()), 
                email=user_data['email'], 
                password=user_data['password']
            ).authenticate_user()
            
            successful_log_in_message = f"Person: {authenticated_user.get_name()} has been logged in"
            request.session['usr_email'] = authenticated_user.get_email()
            messages.success(request, successful_log_in_message)
            return self._go_to_home_page()
        except EmailNotRegisteredException as email_exception:
            messages.error(request, str(email_exception))
        except IncorrectPasswordException as password_exception:
            messages.error(request, str(password_exception))
        
        return self._go_back_to_log_in_page()

    def _go_back_to_log_in_page(self):
        """
        Redirects back to the login page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login page.
        """
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_home_page(self):
        """
        Redirects the user to the home page after successful login.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the home page.
        """
        cardholder_page = reverse('home')
        return redirect(cardholder_page)
