from cardhub.models import CardHolder 
from .InterfaceDao import InterfaceDao as Dao

class CardHolderDao(Dao):
    
    def get(self, email: str) -> CardHolder:
        try: 
            card_holder = CardHolder.objects.get(user=email)
            return card_holder
        except CardHolder.DoesNotExist:
            raise Exception(f'Card holder with id {id} was not found')
    
    def get_all(self) -> list[CardHolder]:
        try:
            card_holders = CardHolder.objects.all()
            return card_holders
        except CardHolder.DoesNotExist:
            raise Exception(f'No card holders were found')
    
    def save(self, card_holder: CardHolder) -> CardHolder:
        try:
            card_holder.save()
            return card_holder
        except Exception as e:
            raise Exception(f'Error saving card holder with id {card_holder.card_holder_id}: {e}')
    
    def update(self, card_holder: CardHolder, data: dict) -> CardHolder:
        try:
            for key, value in data.items():
                setattr(card_holder, key, value)
                card_holder.save()
            return card_holder
        except Exception as e:
            raise Exception(f'Error updating card holder with id {card_holder.id}: {e}')
        
    def delete(self, card_holder: CardHolder) -> CardHolder:
        try:
            card_holder.delete()
            return card_holder
        except Exception as e:
            raise Exception(f'Error deleting card holder with id {card_holder.id}: {e}')
        

    #def remove_card_from_cardholder(self, cardholder_card_id: )