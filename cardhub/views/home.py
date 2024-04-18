
from django.shortcuts import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

class Home(View):
    
    def get(self, request):
        home_view = self._build_home_view(request)
        return home_view

    def _build_home_view(self, request):
        home_view = render(request, 'home.html')
        return home_view

    def post(self, request):
        action = request.POST.get('action')
        if action == 'Log-In':
            return self._go_to_login_page()
        elif action == 'Sign-Up':
            return self._go_to_signup_page()
        else:
            return HttpResponse('Unknown action')
    
    def _go_to_login_page(self):
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_signup_page(self):
        signup_url = reverse('signup')
        return redirect(signup_url)
