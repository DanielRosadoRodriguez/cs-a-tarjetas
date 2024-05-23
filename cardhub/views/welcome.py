
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

class Welcome(View):
    
    def get(self, request):
        welcome_view = self._build_welcome_view(request)
        return welcome_view

    def _build_welcome_view(self, request):
        welcome_view = render(request, 'welcome.html')
        return welcome_view

    def post(self, request):
        action = request.POST.get('action')
        # pasar a polimorfismo
        if action == 'Log-In':
            return self._go_to_login_page()
        elif action == 'Sign-Up':
            return self._go_to_signup_page()
        else:
            ## poner código de error en clases
            return HttpResponse('Unknown action')
    
    def _go_to_login_page(self):
        login_url = reverse('login')
        return redirect(login_url)

    def _go_to_signup_page(self):
        signup_url = reverse('signup')
        return redirect(signup_url)
