from cardhub.models import CreditCardProduct 
from .InterfaceDao import InterfaceDao as Dao

class CreditCardProductDao(Dao):

    def get(self, id: int) -> CreditCardProduct:
        try: 
            card = CreditCardProduct.objects.get(card_id=id)
            return card
        except CreditCardProduct.DoesNotExist:
            raise Exception(f"Card with id {id} was not found")
        
    
    def get_all(self) -> list[CreditCardProduct]:
        try:
            cards = CreditCardProduct.objects.all()
            return cards
        except CreditCardProduct.DoesNotExist:
            raise Exception(f'No cards were found')        
            
    def save(self, card: CreditCardProduct) -> CreditCardProduct:
        try:
            card.save()
            return card
        except Exception as e:
            raise Exception(f'Error saving card with id {card.id}: {e}')
       


    def update(self, card: CreditCardProduct, data: dict) -> CreditCardProduct:
        try:
            for key, value in data.items():
                setattr(card, key, value)
                card.save()
            return card
        except Exception as e:
            raise Exception(f'Error updating card with id {card.id}: {e}')  

    
    def delete(card: CreditCardProduct) -> CreditCardProduct:
        try:    
            card.delete()
            return card
        except Exception as e:
            raise Exception(f'Error deleting card with id {card.id}: {e}')
        

    def build_credit_card_product(self, data: dict) -> CreditCardProduct:
        new_card = CreditCardProduct()
        for key, value in data.items():
            setattr(new_card, key, value)
        return new_card
