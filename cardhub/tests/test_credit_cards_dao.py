from django.http import JsonResponse
from django.test import TransactionTestCase
from cardhub.dao.CreditCardProductDao import CreditCardProductDao
from cardhub.models import CreditCardProduct

class TestCreditCardProductDao(TransactionTestCase):
    def setUp(self):
        self.test_credit_card_product: CreditCardProduct = CreditCardProduct(
            card_id=1,
            card_name='test',
            bank_name='test',
            interest_rate=0.0,
            annuity=0.0
        )  
        self.test_card_values: dict = {'card_name': 'test', 'bank_name': 'test', 'interest_rate': 0.0, 'annuity': 0.0}
        self.test_card_dao: CreditCardProductDao = CreditCardProductDao()
        self.test_card_dao.save(self.test_credit_card_product)


    def test_build_credit_card_product(self):
        expected_response = self.test_credit_card_product
        response: CreditCardProduct = self.test_card_dao.build_credit_card_product(self.test_card_values)
        assert self._are_same_card(response, expected_response)


    def test_save_credit_card_product(self):
        expected_response = self.test_credit_card_product
        response: CreditCardProduct = self.test_card_dao.save(card=self.test_credit_card_product)
        assert response == expected_response


    def test_get_credit_card_product(self):
        expected_response = self.test_credit_card_product
        response: CreditCardProduct = self.test_card_dao.get(id=1)
        assert response == expected_response


    def _are_same_card(self, card1: CreditCardProduct, card2: CreditCardProduct) -> bool:
        return (
            self._have_same_name(card1, card2) and
            self._have_same_bank(card1, card2) and
            self._have_same_interest_rate(card1, card2) and
            self._have_same_annuity(card1, card2)
        )

    def _have_same_name(self, card1: CreditCardProduct, card2: CreditCardProduct) -> bool:
        return card1.card_name == card2.card_name

    def _have_same_bank(self, card1: CreditCardProduct, card2: CreditCardProduct) -> bool:
        return card1.bank_name == card2.bank_name
        
    def _have_same_interest_rate(self, card1: CreditCardProduct, card2: CreditCardProduct) -> bool:
        return card1.interest_rate == card2.interest_rate

    def _have_same_annuity(self, card1: CreditCardProduct, card2: CreditCardProduct) -> bool:
        return card1.annuity == card2.annuity
