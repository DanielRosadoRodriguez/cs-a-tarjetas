
from django.test import TestCase
from cardhub.models import Cardholder, User

class TestUserModel(TestCase):
    def setUp(self):
        self.cardholder = Cardholder.objects.create()
        self.user = User.objects.create(_name="Tyrone Slothrop", 
                                        _email="Tyrone@achtung.com",
                                        _password="password",
                                        _cardholder=self.cardholder)
        
    
    def test_user_get_email(self):
        self.assertEqual(self.user.get_email(), "Tyrone@achtung.com")
        
    def test_user_get_name(self):
        self.assertEqual(self.user.get_name(), "Tyrone Slothrop")
    
    def test_user_get_password(self):
        self.assertEqual(self.user.get_password(), "password")

    def test_set_name(self):
        new_name: str = "Tantivy Mucker-Maffick"
        self.user.set_name(new_name)
        self.assertEqual(self.user.get_name(), new_name)
    
    def test_set_password(self):
        new_password: str = "password2"
        self.user.set_password(new_password)
        self.assertEqual(self.user.get_password(), new_password)
