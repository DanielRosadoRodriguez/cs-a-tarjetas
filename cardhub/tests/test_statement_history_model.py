
from django.test import TestCase
from cardhub.models import BankCard, CardStatement, StatementHistory, User, UserCard


class TestStatementHistoryModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(_name="Maudie Chilkes", 
                                        _email="Maudie@twv.com",
                                        _password="password")
        self.bank_card = BankCard.objects.create(_bank="Visa",
                                                 _name="Azul",
                                                 _interest_rate=0.21)
        self.user_card = UserCard.objects.create(_bank_card=self.bank_card,
                                                    _payment_date="2021-10-10",
                                                    _cut_off_date="2021-10-20",
                                                    _balance=1000,
                                                    _owner=self.user)
        self.statement1 = CardStatement.objects.create(_card=self.user_card,
                                                           _owner_name=self.user_card.get_owner_name(),
                                                           _date="2021-10-10",
                                                           _debt=1000,
                                                           _interest=0.21)
        self.statement2 = CardStatement.objects.create(_card=self.user_card,
                                                              _owner_name=self.user_card.get_owner_name(),
                                                              _date="2021-10-10",
                                                              _debt=700,
                                                              _interest=0.21)
        self.statement3 = CardStatement.objects.create(_card=self.user_card,
                                                                _owner_name=self.user_card.get_owner_name(),
                                                                _date="2021-10-10",
                                                                _debt=100,
                                                                _interest=0.21)
        self.statement_history = StatementHistory.objects.create()
        self.statement_history2 = StatementHistory.objects.create()
        

    # get_all_statements when empty
    def test_get_all_statements_happy_empty(self):
        self.assertEqual(len(self.statement_history2.get_all_statements()), 0)
        self.assertEqual(self.statement_history2.get_all_statements(), [])

    def test_add_statement_happy(self):
        self.statement_history.add_statement(self.statement1)
        self.statement_history.add_statement(self.statement2)
        self.statement_history.add_statement(self.statement3)
        self.assertEqual(len(self.statement_history.get_all_statements()), 3)
        self.assertEqual(self.statement_history.get_all_statements()[0], self.statement1)
        self.assertEqual(self.statement_history.get_all_statements()[1], self.statement2)
        self.assertEqual(self.statement_history.get_all_statements()[2], self.statement3)

    def test_add_statement_sad_wrong_type(self):
        with self.assertRaises(ValueError):
            self.statement_history.add_statement("statement")

