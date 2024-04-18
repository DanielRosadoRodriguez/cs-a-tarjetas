
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
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
            user = self._authenticate_user(user_data) 
            successful_log_in_message = f"Person: { user.get_name() } has been logged in"
            successful_log_in_notification = HttpResponse(successful_log_in_message)
            return successful_log_in_notification
        except Exception as e:
            import traceback
            traceback.print_exc() 
            print(f"An error occurred: {str(e)}")
        return self._go_back_to_log_in_page(request)

    def _authenticate_user(self, user_data):
        auth_user = User.objects.get(_email=user_data['email'], _password=user_data['password'])
        return auth_user
    

    def _go_back_to_log_in_page(self, request):
        log_in_page = render(request, 'login.html', {'form': LogInForm()})
        return log_in_page