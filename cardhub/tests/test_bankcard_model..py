

from django.test import TestCase
from cardhub.models import BankCard

class TestBankcardModel(TestCase):
    def setUp(self):
        self.bankcard = BankCard.objects.create(_bank="Bank of America",
                                                _name="Cash Rewards",
                                                _interest_rate=0.15)
        
    def test_get_id(self):
        self.assertEqual(self.bankcard.get_id(), self.bankcard._id)
    def test_get_bank(self):
        self.assertEqual(self.bankcard.get_bank(), self.bankcard._bank)
    def test_get_name(self):
        self.assertEqual(self.bankcard.get_name(), self.bankcard._name)
    def test_get_interest_rate(self):
        self.assertEqual(self.bankcard.get_interest_rate(), self.bankcard._interest_rate)
    