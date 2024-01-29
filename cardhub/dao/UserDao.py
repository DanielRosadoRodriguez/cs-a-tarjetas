from django.http import JsonResponse
from cardhub.models import User
from .InterfaceDao import InterfaceDao as Dao

class UserDao(Dao):

    def get(self, email: str) -> User:
        return User.objects.get(email=email)


    def get_all(self) -> list[User]:
        users = list(User.objects.all())
        return users


    def save(self, user: User) -> JsonResponse:
        try:
            user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def update(self, user: User, params: dict) -> JsonResponse:
        try:
            user = self.build_user(params) 
            user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def delete(self, user: User) -> JsonResponse:
        try: 
            user.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def build_user(self, params: dict) -> User:
        return User(
            name=params['name'],
            email=params['email'],
            password=params['password']
        )
