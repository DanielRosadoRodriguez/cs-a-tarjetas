"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include(('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cardhub.views.add_card import AddCardView
from cardhub.views.card import Card
from cardhub.views.confirm_card_addition import ConfirmCardAddition
from cardhub.views.confirm_card_deletion import ConfirmCardDeletion
from cardhub.views.delete_card import DeleteCard
from cardhub.views.SignUp import Signup
from cardhub.views.login import Login
from cardhub.views.welcome import Welcome
from cardhub.views.home import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Welcome.as_view(), name='welcome'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_card/', AddCardView.as_view(), name='add_card'),
    path('card_details/', Card.as_view(), name='card'),
    path('delete_card/', DeleteCard.as_view(), name='delete_card'),
    path('confirm_card_deletion/', ConfirmCardDeletion.as_view(), name='confirm_card_deletion'),
    path('confirm_card_addition/', ConfirmCardAddition.as_view(), name='confirm_card_addition'),
]
