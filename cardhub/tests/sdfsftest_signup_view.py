from django.urls import reverse
from django.test import TestCase, Client
from cardhub.models import Cardholder, User

class TestSignupView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_post(self):
        cardholder = Cardholder.objects.create()
        User.objects.create(
            _name='Tyrone',
            _email='Tyrone@achtung.com',
            _password= 'password',
            _cardholder = cardholder
        )

        response = self.client.post(reverse('signup'), {
            '_name': 'Tyrone',
            '_email': 'Tyrone@achtung.com',
            '_password': 'password',
            '_cardholder': cardholder
            })
                        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().get_name(), 'Tyrone')
        self.assertEqual(User.objects.get().get_email(), 'Tyrone@achtung.com')
        self.assertEqual(User.objects.get().get_password(), 'password')
        self.assertEqual(User.objects.get().get_cardholder(), cardholder)
        
    