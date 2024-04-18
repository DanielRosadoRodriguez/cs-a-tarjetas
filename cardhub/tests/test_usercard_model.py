

from django.test import TestCase
from cardhub.models import User, UserCard, BankCard
from cardhub.exceptions.WrongDateFormatException import WrongDateFormatException

class TestUserCard(TestCase):
    def setUp(self):
        self.user = User.objects.create(_email="Tyrone@achtung.com",
                                        _name="Tyrone",
                                        _password="1234")
        self.bank_card = BankCard.objects.create(_bank="Visa",
                                                 _name="Azul",
                                                 _interest_rate=0.21)
        self.bank_card2 = BankCard.objects.create(_bank="Mastercard",
                                                 _name="Roja",
                                                 _interest_rate=0.25)
        self.user_card = UserCard.objects.create(_bank_card=self.bank_card,
                                                 _owner=self.user,
                                                 _payment_date="2021-10-10",
                                                 _cut_off_date="2021-10-20",
                                                 _balance=1000)
        

    # TEST  get_bank_card(self) -> BankCard:
    
    def test_get_bank_card_happy(self):
        self.assertEqual(self.user_card.get_bank_card(), self.bank_card)
    
    def test_get_bank_card_sad(self):
        self.assertNotEqual(self.user_card.get_bank_card(), self.bank_card2)
    
    # TEST  get_payment_date(self) -> str:
    def test_get_payment_date_happy(self):
        self.assertEqual(self.user_card.get_payment_date(), "2021-10-10")
    
    def test_get_payment_date_sad(self):
        self.assertNotEqual(self.user_card.get_payment_date(), "2021-10-20")
    
    # TEST  set_payment_date(self, payment_date: str):
    def test_set_payment_date_happy(self):
        new_payment_date: str = "2021-10-25"
        self.user_card.set_payment_date(new_payment_date)
        self.assertEqual(self.user_card.get_payment_date(), new_payment_date)
        self.assertNotEqual(self.user_card.get_payment_date(), "2021-10-10")

    def test_set_payment_date_sad_not_string(self):
        new_payment_date: str = 20211025
        with self.assertRaises(ValueError):
            self.user_card.set_payment_date(new_payment_date)
            
    def test_payment_date_sad_is_not_after_cut_off_date(self): 
        new_payment_date: str = "2021-10-15"
        with self.assertRaises(ValueError):
            self.user_card.set_payment_date(new_payment_date)

    def test_payment_date_sad_is_not_correct_format(self):
        new_payment_date: str = "102"
        with self.assertRaises(WrongDateFormatException): 
            self.user_card.set_payment_date(new_payment_date)
        
        
    # TEST  get_cut_off_date(self) -> str:

    def test_get_cut_off_date_happy(self):
        self.assertEqual(self.user_card.get_cut_off_date(), "2021-10-20")
    
    # TEST  set_cut_off_date(self, cut_off_date: str):
    def test_set_cut_off_date_happy(self):
        new_cut_off_date = "1000-01-01"
        old_cut_off_date = self.user_card.get_cut_off_date()
        self.user_card.set_cut_off_date(new_cut_off_date)
        self.assertEqual(self.user_card.get_cut_off_date(), new_cut_off_date)
        self.assertNotEqual(self.user_card.get_cut_off_date(), old_cut_off_date)

    def test_set_cut_off_date_sad_is_not_string(self):
        new_cut_off_date = 10394549
        with self.assertRaises(ValueError):
            self.user_card.set_cut_off_date(new_cut_off_date)

    def test_set_cut_off_date_sad_is_not_before_payment_date(self):
        new_cut_off_date = "2022-01-01"
        with self.assertRaises(ValueError):
            self.user_card.set_cut_off_date(new_cut_off_date)
    
    def test_set_cut_off_date_sad_is_not_correct_format(self):
        new_cut_off_date = "22/02/20"
        with self.assertRaises(WrongDateFormatException):
            self.user_card.set_cut_off_date(new_cut_off_date)

    # TEST  get_balance(self) -> float:
    def test_get_balance_happy(self):
        balance = self.user_card.get_balance()
        expected_balance = 1000
        self.assertEqual(balance, expected_balance)
    
    def test_get_balance_sad(self):
        balance = self.user_card.get_balance()
        expected_balance = 100
        self.assertNotEqual(balance, expected_balance)
        
    # TEST  pay(self, payment: float):

    def test_pay_happy(self):
        payment = float(500)
        self.user_card.pay(payment)
        self.assertEqual(self.user_card.get_balance(), 500)
    
    def test_pay_happy2(self):
        payment = float(1000)
        self.user_card.pay(payment)
        self.assertEqual(self.user_card.get_balance(), 0)

    def test_pay_happy3(self):
        payment = float(700)
        self.user_card.pay(payment)
        self.assertEqual(self.user_card.get_balance(), 300)
        
    def test_pay_sad_payment_is_too_big(self):
        payment = float(2000)
        with self.assertRaises(ValueError):
            self.user_card.pay(payment)
    
    def test_pay_sad_payment_is_not_float(self):
        payment = 2000
        with self.assertRaises(ValueError):
            self.user_card.pay(payment)
    
    def test_pay_sad_payment_is_negative(self):
        payment = float(-200)
        with self.assertRaises(ValueError):
            self.user_card.pay(payment)
 