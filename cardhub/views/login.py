
from django.http import HttpResponse
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
 
    def get(self, request):
        log_in_view = self._build_log_in_view(request)
        return log_in_view

    def _build_log_in_view(self, request):
        log_in_form = LogInForm()
        log_in_view = render(request, 'login.html', {'form': log_in_form})
        return log_in_view

    def post(self, request):
        _log_in_user_response = self._log_in_user(request)
        return _log_in_user_response

    def _log_in_user(self, request):
        form = LogInForm(request.POST)
        if not form.is_valid(): return self._go_back_to_log_in_page(request)
        user_data = form.cleaned_data
        try:
            authenticated_user = Authenticator(users=list(User.objects.all()), email=user_data['email'], password=user_data['password']).authenticate_user()
            successful_log_in_message = f"Person: { authenticated_user.get_name() } has been logged in"
            messages.success(request, successful_log_in_message)
            return self._go_to_cardholder_page(request)
        except EmailNotRegisteredException as email_exception:
            messages.error(request, str(email_exception))
        except IncorrectPasswordException as password_exception:
            messages.error(request, str(password_exception))
        return self._go_back_to_log_in_page(request)
    

    def _go_back_to_log_in_page(self):
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_cardholder_page(self, request):
        cardholder_page = render(request, 'cardholder.html')
        return cardholder_page