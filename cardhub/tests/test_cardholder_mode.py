
from django.test import TestCase

from cardhub.models import BankCard, Cardholder, User, UserCard

class TestCardholderModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(_name="Sir Stephen Dodson-Truck",
                                        _email="Stephen@fopid.com",
                                        _password="password")
        self.bank_card1 = BankCard.objects.create(_bank="Chase",
                                                 _name="Freedom Unlimited",
                                                 _interest_rate=0.2)
        self.bank_card2 = BankCard.objects.create(_bank="Chase",
                                                 _name="Blue",
                                                 _interest_rate=0.2)
        self.bank_card3 = BankCard.objects.create(_bank="Chase",
                                                    _name="Sapphire",
                                                    _interest_rate=0.5)
        self.user_card1 = UserCard.objects.create(_bank_card=self.bank_card1,
                                                _owner=self.user,
                                                _payment_date="2020-01-01",
                                                _cut_off_date="2020-01-15",
                                                _balance=1000)                                                                                    
        self.user_card2 = UserCard.objects.create(_bank_card=self.bank_card2,
                                                _owner=self.user,
                                                _payment_date="2020-02-01",
                                                _cut_off_date="2020-02-15",
                                                _balance=2000)
        self.user_card3 = UserCard.objects.create(_bank_card=self.bank_card3,
                                                _owner=self.user,
                                                _payment_date="2020-03-01",
                                                _cut_off_date="2020-03-15",
                                                _balance=3000)
        self.cardholder = Cardholder.objects.create()
        self.cardholder2 = Cardholder.objects.create()
        self.cardholder3 = Cardholder.objects.create()

        self.cardholder3.add_card(self.user_card1)

        self.cardholder4 = Cardholder.objects.create()
        self.cardholder4.add_card(self.user_card1)
        self.cardholder4.add_card(self.user_card2)
        self.cardholder4.add_card(self.user_card3)
        

    # def add_card(self, card: UserCard):
    def test_add_card_happy(self):
        self.cardholder.add_card(self.user_card1)
        self.assertEqual(self.cardholder.get_all_cards(), [self.user_card1])
    
    def test_add_card_happy_multiple(self):
        self.cardholder2.add_card(self.user_card1)
        self.cardholder2.add_card(self.user_card2)
        self.assertEqual(self.cardholder2.get_all_cards(), [self.user_card1, self.user_card2])

    def test_add_card_sad_not_card(self):
        with self.assertRaises(ValueError):
            self.cardholder.add_card("Not a card")
        
    # def get_all_cards(self) -> list[UserCard]:
    def test_get_all_cards_happy(self):
        self.assertEqual(self.cardholder3.get_all_cards(), [self.user_card1])
    
    def test_get_all_cards_happy_multiple(self):
        self.assertEqual(self.cardholder4.get_all_cards(), [self.user_card1, self.user_card2, self.user_card3])

   # def get_card_by_name(self, name: str) -> UserCard:
    def test_get_card_by_name_happy(self):
        self.assertEqual(self.cardholder4.get_card_by_name("Freedom Unlimited"), self.user_card1)
        self.assertEqual(self.cardholder4.get_card_by_name("Blue"), self.user_card2)
        self.assertEqual(self.cardholder4.get_card_by_name("Sapphire"), self.user_card3)

    # def remove_card(self, card: UserCard):
    def test_remove_card_happy(self):
        self.cardholder4.remove_card(self.user_card1)
        self.assertEqual(self.cardholder4.get_all_cards(), [self.user_card2, self.user_card3])
    
    def test_remove_card_happy_multiple(self):
        self.cardholder4.remove_card(self.user_card1)
        self.cardholder4.remove_card(self.user_card2)
        self.assertEqual(self.cardholder4.get_all_cards(), [self.user_card3])
    
    def test_remove_card_sad_not_card(self):
        with self.assertRaises(ValueError):
            self.cardholder4.remove_card("Not a card")

    
