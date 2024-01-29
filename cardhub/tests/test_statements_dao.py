import json
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.test import TransactionTestCase
from cardhub.dao.AccountStatementDao import AccountStatementDao
from cardhub.models import AccountStatement, CardHolder, CardHolderCard, CreditCardProduct, User

class TestUserDao(TransactionTestCase):
    def setUp(self):
        self.expected_response = JsonResponse({'status': 'success'})
        self._init_test_values_db()


    def test_get_stetement_w_all_params(self):
        cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=1)
        params = {
            'date': '2021-05-01',
            'cut_off_date': '2021-05-15',
            'payment_date': '2021-05-30',
            'current_debt': 10000.00,
            'pni': 5000.00,
            'card_from_cardholder': cardholder_card
        }
        statement = AccountStatementDao().build_card_statement(params)
        response = AccountStatementDao().save(statement)
        assert response.content == self.expected_response.content


    def test_create_statement_w_some_params(self):
        cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=1)
        params = {
            'date': '2021-05-01',
            'cut_off_date': '2021-05-15',
            'payment_date': None,
            'current_debt': None,
            'pni': None,
            'card_from_cardholder': cardholder_card
        }
        statement = AccountStatementDao().build_card_statement(params)
        response = AccountStatementDao().save(statement)
        assert response.content == self.expected_response.content


    def test_create_statement_without_params(self):
        cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=1)
        params = {
            'date': None,
            'cut_off_date': None,
            'payment_date': None,
            'current_debt': None,
            'pni': None,
            'card_from_cardholder': cardholder_card
        }
        statement = AccountStatementDao().build_card_statement(params)
        response = AccountStatementDao().save(statement)
        assert response.content == self.expected_response.content
    
    
    def test_get_all_user_statements(self):
        response = AccountStatementDao().get_all_user_statements(self.test_user.email)
        assert response.status_code == 200

    
    def test_get_cardholder_statements(self):
        response = AccountStatementDao().get_cardholder_statements(self.test_cardholder_card.card_holder_cards_id)
        assert response.status_code == 200


    def test_get_last_card_statement(self):
        response = AccountStatementDao().get_last_card_statement(self.test_cardholder_card.card_holder_cards_id)
        assert response.status_code == 200
        

    def _init_test_values_db(self):
        self.test_user = User(
            name='test_user',
            email='joselito@joselito.com',
            password='test_password'
        )
        self.test_cardholder = CardHolder(
            user=self.test_user
        )
        self.test_card = CreditCardProduct(
            card_id=1,
            card_name='test_card',
            bank_name='test_bank',
            interest_rate=0.00,
            annuity=0.00
        )
        self.test_cardholder_card = CardHolderCard(
            card_holder_cards_id=1,
            card_holder=self.test_cardholder,
            card=self.test_card
        )

        self.test_user.save()
        self.test_card.save()
        self.test_cardholder.save()
        self.test_cardholder_card.save()

        self.test_statement = AccountStatement(
            date='2021-05-01',
            cut_off_date='2021-05-15',
            payment_date='2021-05-30',
            current_debt=10000.00,
            payment_for_no_interest=5000.00,
            card_from_cardholder=self.test_cardholder_card
        )

        self.test_statement.save()
