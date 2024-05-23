
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class Welcome(View):
    """
    View for rendering the welcome page.

    This class-based view handles GET requests to render the welcome page,
    which provides options for logging in or signing up. It also handles
    POST requests to redirect the user based on their chosen action.

    Methods
    -------
    get(request)
        Handles GET requests to render the welcome page.

    post(request)
        Handles POST requests to redirect the user based on their chosen action.
    """
    
    def get(self, request):
        """
        Handles GET requests to render the welcome page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the GET request data.

        Returns
        -------
        HttpResponse
            The rendered welcome view.
        """
        welcome_view = self._build_welcome_view(request)
        return welcome_view

    def _build_welcome_view(self, request):
        """
        Constructs the welcome view.

        Parameters
        ----------
        request : HttpRequest
            The request object used to generate this response.

        Returns
        -------
        HttpResponse
            The rendered welcome view.
        """
        welcome_view = render(request, 'welcome.html')
        return welcome_view

    def post(self, request):
        """
        Handles POST requests to redirect the user based on their chosen action.

        Parameters
        ----------
        request : HttpRequest
            The request object containing the POST request data.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login or signup page.
        """
        action = request.POST.get('action')
        if action == 'Log-In':
            return self._go_to_login_page()
        elif action == 'Sign-Up':
            return self._go_to_signup_page()
        else:
            return HttpResponse('Unknown action')
    
    def _go_to_login_page(self):
        """
        Redirects to the login page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the login page.
        """
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_signup_page(self):
        """
        Redirects to the signup page.

        Returns
        -------
        HttpResponseRedirect
            A redirect response to the signup page.
        """
        signup_url = reverse('signup')
        return redirect(signup_url)
