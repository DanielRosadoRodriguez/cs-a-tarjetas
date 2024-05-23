from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from cardhub.forms import UserForm
from cardhub.models import Cardholder, User
from django.contrib import messages
from django.db.utils import IntegrityError


class Signup(View):
    """
    View for handling user signup.

    This class-based view handles GET and POST requests for the signup page.
    It renders the signup form and processes user registration.

    Methods
    -------
    get(request)
        Handles GET requests to render the signup page.
    
    post(request)
        Handles POST requests to register the user.
    """
    
    def get(self, request):
        """
        Handles GET requests to render the signup page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the GET request data.

        Returns
        -------
        HttpResponse
            The rendered signup view with an empty signup form.
        """
        sign_up_view = self._build_signup_view(request)
        return sign_up_view

    def _build_signup_view(self, request):
        """
        Constructs the signup view with an empty signup form.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered signup view with an empty signup form.
        """
        sign_up_form = UserForm()
        sign_up_view = render(request, 'signup.html', {'form': sign_up_form})
        return sign_up_view

    def post(self, request):
        """
        Handles POST requests to register the user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST request data.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login page if registration is successful,
            or back to the signup page if registration fails.
        """
        _register_user_response = self._register_user(request)
        return _register_user_response

    def _register_user(self, request):  
        """
        Processes user registration based on the submitted signup form.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST data with the signup form.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login page if registration is successful,
            or back to the signup page if registration fails.
        """
        form = UserForm(request.POST)
        if not form.is_valid():
            return self._go_back_to_signup_page()
        
        new_user_data = form.cleaned_data
        if not self._is_new_email(request, new_user_data):
            return self._go_back_to_signup_page()
        
        try:
            self._save_user(new_user_data)
            self._send_success_message(request)
            return self._go_to_login_page()
        except IntegrityError as e:
            integrity_error_message = "Integrity Error, contact support"
            self._send_error_message(request, integrity_error_message)
            return self._go_back_to_signup_page(request)

    def _go_to_login_page(self):
        """
        Redirects to the login page after successful registration.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login page.
        """
        login_url = reverse('login')
        return redirect(login_url)

    def _is_new_email(self, request, new_user_data):
        """
        Checks if the entered email is not already registered.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST data with the signup form.
        new_user_data : dict
            Dictionary containing the form data for the new user.

        Returns
        -------
        bool
            True if the email is new, False if it's already registered.
        """
        given_email = new_user_data['email']
        if User.objects.filter(_email=given_email):
            error_message = "This email is already registered, please enter a new one."
            self._send_error_message(request, error_message=error_message)
            return False
        else:
            return True
        
    def _send_success_message(self, request):
        """
        Sends a success message to the user.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the form submission data.
        """
        success_message = 'User created successfully'
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
        
    def _go_back_to_signup_page(self):
        """
        Redirects back to the signup page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the signup page.
        """
        signup_url = reverse('signup')
        return redirect(signup_url)
        
    def _save_user(self, data):
        """
        Saves the new user and associated cardholder in the database.

        Parameters
        ----------
        data : dict
            Dictionary containing the form data for the new user.

        Returns
        -------
        User
            The newly created User object.
        """
        cardholder = Cardholder.objects.create()
        user = User.objects.create(
            _name=data['name'],
            _email=data['email'],
            _password=data['password'],
            _cardholder=cardholder
        )
        return user
