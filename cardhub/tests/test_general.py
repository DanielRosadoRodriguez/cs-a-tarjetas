from cardhub.dao.CreditCardProductDao import CreditCardProductDao
from ..models import CreditCardProduct
from django.test import TransactionTestCase


class TestGeneral(TransactionTestCase):
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
    
    def test_get_all_cards(self):
        expected = CreditCardProduct.objects.all()
        received = CreditCardProductDao().get_all()
        assert list(expected.values()) == list(received.values())
    