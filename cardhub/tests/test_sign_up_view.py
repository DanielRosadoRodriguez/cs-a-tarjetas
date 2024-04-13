from django.urls import reverse
from django.test import TestCase, Client
from cardhub.models import User

class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add.html')

    def test_post(self):
        User.objects.create(
            name='Tyrone',
            email='Tyrone@achtung.com',
            password= 'password'
        )

        response = self.client.post(reverse('signup'), {
            'name': 'Tyrone',
            'email': 'Tyrone@achtung.com',
            'password': 'password'
            })
                        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Tyrone')
        self.assertEqual(User.objects.get().email, 'Tyrone@achtung.com')
        self.assertEqual(User.objects.get().password, 'password')
        
    