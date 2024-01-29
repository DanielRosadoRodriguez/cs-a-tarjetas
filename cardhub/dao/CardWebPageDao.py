from cardhub.models import CardWebPage
from .InterfaceDao import InterfaceDao as Dao

class CardWebpageDao(Dao):

    def get(self, id: int) -> CardWebPage:
        try: 
            card_webpage = CardWebPage.objects.get(id=id)
            return card_webpage
        except CardWebPage.DoesNotExist:
            raise Exception(f'Card webpage with id {id} was not found')
    
    def get_all(self) -> list[CardWebPage]:
        try:
            card_webpages = CardWebPage.objects.all()
            return card_webpages
        except CardWebPage.DoesNotExist:
            raise Exception(f'No card webpages were found')
    
    def save(self, card_webpage: CardWebPage) -> CardWebPage:
        try:
            card_webpage.save()
            return card_webpage
        except Exception as e:
            raise Exception(f'Error saving card webpage with id {card_webpage.id}: {e}')
        
    def update(self, card_webpage: CardWebPage, data: dict) -> CardWebPage:
        try:
            for key, value in data.items():
                setattr(card_webpage, key, value)
                card_webpage.save()
            return card_webpage
        except Exception as e:
            raise Exception(f'Error updating card webpage with id {card_webpage.id}: {e}')
    
    def delete(self, card_webpage: CardWebPage) -> CardWebPage:
        try:
            card_webpage.delete()
            return card_webpage
        except Exception as e:
            raise Exception(f'Error deleting card webpage with id {card_webpage.id}: {e}')
    
    