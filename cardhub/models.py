from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    

class CreditCardProduct(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    annuity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    
    
class CardHolder(models.Model):
    card_holder_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def add_card(self, card: CreditCardProduct):
        card_holder_card = CardHolderCard.objects.create(card_holder=self, card=card)
        return card_holder_card
    
    def remove_card(self, card: CreditCardProduct):
        deleted_cardholder_card = CardHolderCard.objects.get(card_holder=self, card=card).delete()
        return deleted_cardholder_card
    
    def get_cards(self):
        return CardHolderCard.objects.filter(card_holder=self)
    

class CardHolderCard(models.Model):
    card_holder_cards_id = models.AutoField(primary_key=True)
    card_holder = models.ForeignKey(CardHolder, on_delete=models.CASCADE)
    card = models.ForeignKey(CreditCardProduct, on_delete=models.CASCADE)


class CardWebPage(models.Model):
    pageID = models.AutoField(primary_key=True)
    page_url = models.CharField(max_length=100)
    page_content = models.TextField()
    associated_cards = models.ForeignKey(CreditCardProduct, on_delete=models.CASCADE)


class AccountStatement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    date = models.DateField(null=True)
    cut_off_date = models.DateField(null=True)
    payment_date = models.DateField(null=True)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_for_no_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    card_from_cardholder = models.ForeignKey(CardHolderCard, on_delete=models.CASCADE)
