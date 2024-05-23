from django.shortcuts import redirect, render
from django.views import View
from cardhub.models import UserCard
from django.urls import reverse
from django.shortcuts import redirect, render
from cardhub.models import UserCard, WrongDateFormatException, BankCard
from datetime import date, datetime
from django.contrib import messages


class EditCard(View):


    def post(self, request):
        if 'cancel' in request.POST:
            return self._go_to_home_page()
        elif 'save_changes' in request.POST:
            card_id = request.POST['card_id']
            new_cut_off_date = request.POST.get('new_cut_off_date')
            new_payment_date = request.POST.get('new_payment_date')
            self.edit(request, new_cut_off_date, new_payment_date)
            return self._go_to_card_details(request)
        else:
            return self._build_response(request)


    def _build_response(self, request):
        user_card = self._query_user_card(request)
        user_card_view = render(request, 'edit_card.html', {'user_card': user_card})
        return user_card_view

    def _query_user_card(self, request):
        card_id = request.POST['card_id']  
        user_card = UserCard.objects.get(_id=card_id)
        return user_card
    
    def _go_to_home_page(self):
        home_url = reverse('home')
        return redirect(home_url)
    
    def _go_to_card_details(self, request):
        request.session['card_id'] = request.POST['card_id']
        card_details_url = reverse('card_details')
        return redirect(card_details_url)

    
    def date_to_str(self, input_date):
        # Validate parameter
        if not input_date: raise ValueError("Input date can't be empty")
        # Verify parameter type
        if not isinstance(input_date, date): raise ValueError("Cut off date must be a date")
        return input_date.strftime('%Y-%m-%d')

    def str_to_date(self, str_date):
        return datetime.strptime(str_date, '%Y-%m-%d').date()

    def edit (self, request, new_cut_off_date, new_payment_date):
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
        success_message:str =  'Changes saved successfully'
        messages.success(request, success_message)
    
    def _send_error_message(self, request, error_message):
        messages.error(request, error_message)
        