from .app_views.ViewModifyStatement import ViewModifyStatement
from .app_views.ViewGenerateCardStatement import ViewGenerateCardStatement
from .app_views.ViewGetAllUserCards import GetAllUserCards
from .app_views.ViewRemoveCardFromCardholder import RemoveCardFromCardholder
from .app_views.ViewGetLastStatement import GetLastStatement
from .app_views.ViewSignUp import ViewSignUp
from .app_views.ViewLogin import ViewLogin
from .app_views.ViewGetAllCards import ViewGetAllCards
from .app_views.ViewAddCardToCardholder import ViewAddCardToCardholder
from .app_views.ViewGetAllStatementsFromCard import ViewGetAllStatementsFromCard



from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signup(request):
    return ViewSignUp(request).generate_json_response()
    

@csrf_exempt
def login(request):
    return ViewLogin(request).generate_json_response()


@csrf_exempt
def add_card_to_user_cardholder(request):
    return ViewAddCardToCardholder(request).generate_json_response()

        
@csrf_exempt
def remove_card_from_cardholder(request):
    return RemoveCardFromCardholder(request).generate_json_response()


@csrf_exempt
def generate_card_statement(request):
    return ViewGenerateCardStatement(request).generate_json_response()


@csrf_exempt
def get_all_cards(request):
    return ViewGetAllCards().generate_json_response()


@csrf_exempt
def get_all_user_cards(request):
    return GetAllUserCards(request).generate_json_response()


@csrf_exempt
def get_last_statement(request):
    return GetLastStatement(request).generate_json_response()


@csrf_exempt
def get_all_statement_from_card(request):
    return ViewGetAllStatementsFromCard(request).generate_json_response()


@csrf_exempt    
def modify_statement(request):
    return ViewModifyStatement(request).generate_json_response()
