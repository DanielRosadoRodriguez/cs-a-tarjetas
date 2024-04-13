from django.http import JsonResponse
from django.test import TransactionTestCase
from cardhub.dao.UserDao import UserDao
from cardhub.models import User

class TestUserDao(TransactionTestCase):
    
    def setUp(self):
        self.test_user: User = User(
            name='test',
            email='test@test.com',
            password='testpassword'
        )  
        self.test_users: list[User] = self._build_test_users()
        self.user_dao: UserDao = UserDao()
    
    
    def test_save_user(self):
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        response:JsonResponse = self.user_dao.save(user=self.test_user)
        assert response.content == expected_response.content

    
    def test_get_user(self):
        expected_user = self.test_user
        self.user_dao.save(user=self.test_user)
        response_user: User = UserDao().get('test@test.com')
        assert response_user == expected_user


    def test_get_all_users(self):
        expected_users = self.test_users
        self._save_every_user(users=expected_users)
        response_users: list[User] = self.user_dao.get_all()
        assert response_users == expected_users

        
    def test_update_user_name(self):
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        self.user_dao.save(user=self.test_user)
        new_name = 'new_test_name'
        response_update = self.user_dao.update(user=self.test_user, params={'email':self.test_user.email, 'name': new_name, 'password': self.test_user.password})
        response_user: User = UserDao().get(self.test_user.email)
        assert response_user.name == new_name and response_update.content == expected_response.content
                
                
    def test_update_user_password(self):
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        self.user_dao.save(user=self.test_user)
        new_password = 'new_test_password'
        response_update = self.user_dao.update(user=self.test_user, params={'email':self.test_user.email, 'name': self.test_user.name, 'password': new_password})
        response_user: User = UserDao().get(self.test_user.email)
        assert response_user.password == new_password and response_update.content == expected_response.content


    def test_delete_user(self):
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        self.user_dao.save(user=self.test_user)
        response_delete = self.user_dao.delete(user=self.test_user)
        assert response_delete.content == expected_response.content
        
        
    def _build_test_users(self):
        return [ 
            User(
                name=f'test{i}',
                email=f'test{i}@test.com',
                password=f'testpassword{i}'
            )
            for i in range(1, 4)
        ]


    def _save_every_user(self, users: list[User]):
        for user in users:
            self.user_dao.save(user=user)
