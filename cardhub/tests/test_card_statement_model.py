
from django.test import TestCase

from cardhub.models import BankCard, CardStatement, User, UserCard


class TestCardStatementModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(_name="Nora Dodstone-Truck",
                                        _email="Nora@twv.com",
                                        _password="password")
        self.bank_card = BankCard.objects.create(_bank="Visa",
                                                 _name="Azul",
                                                 _interest_rate=0.21)
        self.bank_card2 = BankCard.objects.create(_bank="Mastercard",
                                                 _name="Azul",
                                                 _interest_rate=0.21)
        self.user_card = UserCard.objects.create(_bank_card=self.bank_card,
                                                 _payment_date="2021-10-10",
                                                 _cut_off_date="2021-10-20",
                                                 _balance=1000,
                                                _owner=self.user)
        self.card_statement = CardStatement.objects.create(_card=self.user_card,
                                                           _owner_name =self.user_card.get_owner_name(),
                                                           _date="2021-10-10",
                                                           _debt=1000,
                                                           _interest=0.21)
                                                           


    #def get_card(self) -> UserCard:
    def test_get_card_happy(self):
        self.assertEqual(self.card_statement.get_card(), self.user_card)
    
    def test_get_card_sad(self):
        self.assertNotEqual(self.card_statement.get_card(), self.bank_card2)

    #def get_username(self) -> str:
    def test_get_username_happy(self):
        self.assertEqual(self.card_statement.get_owner_name(), self.user.get_name())

    def test_get_username_sad(self):
        self.assertNotEqual(self.card_statement.get_owner_name(), "Grigori")

    # #def get_statement_date(self) -> str:

    def test_get_statement_date_happy(self):
        self.assertEqual(self.card_statement.get_date(), "2021-10-10")

    def test_get_statement_date_sad(self):
        self.assertNotEqual(self.card_statement.get_date(), "2021-10-20")
    
    # #def get_debt(self) -> float:
    def test_get_debt_happy(self):
        self.assertEqual(self.card_statement.get_debt(), 1000)
    
    def test_get_debt_sad(self):
        self.assertNotEqual(self.card_statement.get_debt(), 2000)

    # #def get_interest(self) -> float:
    def test_get_interest_happy(self):
        self.assertEqual(self.card_statement.get_interest(), 0.21)
    
    def test_get_interest_sad(self):
        self.assertNotEqual(self.card_statement.get_interest(), 0.25)
    
    
