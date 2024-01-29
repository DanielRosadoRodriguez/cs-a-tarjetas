from django.forms import model_to_dict
from django.http import JsonResponse
from cardhub.models import AccountStatement, CardHolder, CardHolderCard, User 
from .InterfaceDao import InterfaceDao as Dao

class AccountStatementDao(Dao):

    def get(self, id: int) -> AccountStatement:
        return AccountStatement.objects.get(statement_id=id)


    def get_all(self) -> list[AccountStatement]:
        card_statements = list(AccountStatement.objects.all())
        return card_statements


    def save(self, card_statement: AccountStatement) -> JsonResponse:
        try:
            card_statement.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            message = e.__str__()
            return JsonResponse({'status': 'error', 'message': message})


    def update(self, card_statement: AccountStatement, params: dict) -> JsonResponse:
        try:
            card_statement.date = params.get('date')
            card_statement.cut_off_date = params.get('cut_off_date')
            card_statement.payment_date = params.get('payment_date')
            card_statement.current_debt = params.get('current_debt')
            card_statement.payment_for_no_interest = params.get('pni')
            card_statement.save()
            statement_dict = model_to_dict(card_statement)
            statement_response = list([statement_dict])
            return JsonResponse(statement_response, safe=False) 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def delete(self, card_statement: AccountStatement) -> JsonResponse:
        try: 
            card_statement.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def get_all_user_statements(self, user_email: str) -> list[AccountStatement]:
        user = User.objects.get(email=user_email)
        card_holder = CardHolder.objects.get(user=user)
        card_holder_cards = CardHolderCard.objects.filter(card_holder=card_holder)
        statements = AccountStatement.objects.filter(card_from_cardholder__in=card_holder_cards)
        statements_val = statements.values()
        statements_as_list = list(statements_val)
        statements_as_json = JsonResponse(statements_as_list, safe=False)
        return statements_as_json
    
    
    def build_card_statement(self, params: dict) -> AccountStatement:
        return AccountStatement(
            statement_id = params.get('statement_id'),
            date = params.get('date'),
            cut_off_date = params.get('cut_off_date'),
            payment_date = params.get('payment_date'),
            current_debt = params.get('current_debt'),
            payment_for_no_interest = params.get('pni'),
            card_from_cardholder = params.get('card_from_cardholder')
        )
    

    def get_cardholder_statements(self, cardholder_card_id: int) -> AccountStatement:
        cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=cardholder_card_id)
        statements = list(AccountStatement.objects.filter(card_from_cardholder=cardholder_card).values())
        statements_as_json = JsonResponse(statements, safe=False)
        return statements_as_json


    def get_last_card_statement(self, cardholder_card_id: int) -> AccountStatement:
        try: 
            statement = AccountStatement.objects.filter(card_from_cardholder=cardholder_card_id).order_by('-statement_id')[0]
            statement_dict = model_to_dict(statement)
            statement_response = list([statement_dict])
            return JsonResponse(statement_response, safe=False) 
        except IndexError:
            return JsonResponse({'status': 'error', 'message': 'No statements found for the given cardholder_card_id'}, status=404)
        

    