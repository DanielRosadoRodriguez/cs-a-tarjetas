from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from cardhub.models import UserCard, AccountStatement

class AccountStatementView(View):

    def get(self, request, card_id):
        user_card = get_object_or_404(UserCard, _id=card_id)
        statement, created = AccountStatement.objects.get_or_create(card=user_card)
        
        """Buena práctica: Manejo de errores desde la URL de la solicitud"""
        context = {
            'statement': statement,
            'user_card': user_card,
            'errors': request.GET.get('errors', '')
        }
        
        return render(request, 'account_statement.html', context)

    def post(self, request, card_id):
        user_card = get_object_or_404(UserCard, _id=card_id)
        statement, created = AccountStatement.objects.get_or_create(card=user_card)

        """ Buena práctica: Captura de datos POST de forma segura"""
        payment = request.POST.get('payment_amount')
        charge = request.POST.get('charge_amount')
        errors = []

        try:
            """ Manejo de cargos"""
            if charge:
                amount = float(charge)
                statement.add_charge(amount)
                
            """ Manejo de pagos"""
            if payment:
                payment_amount = float(payment)
                if not user_card._is_correct_payment(payment_amount):
                    raise ValueError("Invalid payment.")
                user_card.pay(payment_amount)
                statement.add_payment(payment_amount)
        except Exception as e:
            errors.append(str(e))

        """ Buena práctica: Redirección con manejo de errores"""
        if errors:
            return redirect(f"{request.path}?errors={' '.join(errors)}")
        return redirect('account_statement', card_id=card_id)  # Añadir URL


