import re
from django.db import models
from cardhub.exceptions.CardNotFoundError import CardNotFoundError
from cardhub.exceptions.WrongDateFormatException import WrongDateFormatException
from datetime import date



class BankCard(models.Model):
    '''
    ADT: Tarjeta de banco
    Def: En el contexto del problema, 
        representa a las tarjetas de banco disponibles 
        para que el usuario agregue a su tarjetero. 
        Debido a la naturaleza del producto, 
        todas las tarjetas de banco son tarjetas de crédito. 
        Nota: debido a que los valores asignados a la
        tarjeta en sus respectivos atributos se obtienen 
        de una base de datos pre-armada, 
        estos no son modificables. 

    '''
    _id = models.AutoField(primary_key=True)
    _bank = models.CharField(max_length=100, null=False)
    _name = models.CharField(max_length=100, null=False)
    _interest_rate = models.FloatField(null=False)
    
    def get_id(self) -> int:
        '''
        IN: None
        OUT: int
        Def: Permite obtener el identificador único de la tarjeta de banco.
        '''
        return self._id

    def get_bank(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre del banco al que pertenece la tarjeta de banco.
        '''
        return self._bank

    def get_name(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre de la tarjeta de banco.
        '''
        return self._name

    def get_interest_rate(self) -> float:
        '''
        IN: None
        OUT: float
        Def: Permite obtener la tasa de interés de la tarjeta de banco.
        '''
        return self._interest_rate


class UserCard(models.Model):
    '''
    ADT: Tarjeta de usuario
    Def: Representa una tarjeta en posesión de un usuario de la aplicación. 
    Dado el contexto del problema 
    (la aplicación solo permite la gestión de tarjetas de crédito) 
    todas las tarjetas de usuario son, 
    necesariamente, una tarjeta de crédito. 
    El usuario puede poseer únicamente una copia de una misma tarjeta de banco 
    (e. g. Si el usuario posee una tarjeta de banco “BBVA Azúl", 
    no puede agregar otra tarjeta de banco “BBVA Azúl” a su tarjetero). 
    '''
    _id = models.AutoField(primary_key=True)
    _bank_card = models.ForeignKey(BankCard, on_delete=models.CASCADE)
    _owner = models.ForeignKey('User', on_delete=models.CASCADE)
    _payment_date = models.DateField(null=False) #The format is YYYY-MM-DD
    _cut_off_date = models.DateField(null=False) #The format is YYYY-MM-DD
    _balance = models.FloatField(null=False)
    _statement_history = models.OneToOneField('StatementHistory', on_delete=models.CASCADE, null=True)

    def get_statement_history(self) -> 'StatementHistory':
        '''
        IN: None
        OUT: StatementHistory
        Def: Permite obtener el historial de estados de la tarjeta de usuario.
        '''
        return self._statement_history
    
    def get_id(self) -> int:
        '''
        IN: None
        OUT: int
        Def: Permite obtener el identificador único de la tarjeta de usuario.
        '''
        return self._id
    
    def get_owner_name(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre del propietario de la tarjeta de usuario.
        '''
        return self._owner.get_name()
    
    def get_owner(self) -> 'User':
        '''
        IN: None
        OUT: User
        Def: Permite obtener el propietario de la tarjeta de usuario.
        '''
        return self._owner

    def get_bank_card(self) -> BankCard:
        '''
        IN: None
        OUT: BankCard
        Def: Permite obtener la tarjeta de banco asociada a la tarjeta de usuario.
        '''
        return self._bank_card
    
    def get_name(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre de la tarjeta de banco asociada a la tarjeta de usuario.
        '''
        return self._bank_card.get_name()
    
    def get_bank(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre del banco al que pertenece la tarjeta de banco asociada a la tarjeta de usuario.
        '''
        return self._bank_card.get_bank()
    
    def get_payment_date(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la fecha de pago de la tarjeta de usuario.
        '''
        return self._payment_date

    def set_payment_date(self, payment_date: str):
        '''
        IN: str
        OUT: None
        Def: Permite establecer la fecha de pago de la tarjeta de usuario.
        '''
        # Verify parameter
        if not payment_date: raise ValueError("Payment date can't be empty")
        # Validate parameter type
        if not self._is_valid_payment_date(payment_date): raise ValueError("Incorrect payment date")

        # Set the payment date
        self._payment_date = payment_date
        self.save()

    def get_cut_off_date(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la fecha de corte de la tarjeta de usuario.
        '''
        return self._cut_off_date   

    def set_cut_off_date(self, cut_off_date: str):
        '''
        IN: str
        OUT: None
        Def: Permite establecer la fecha de corte de la tarjeta de usuario.
        '''
        # Validate parameter
        if not cut_off_date: raise ValueError("Cut off date can't be empty")
        # Verify parameter
        if not self._is_valid_cut_off_date(cut_off_date): raise ValueError("Incorrect cut off date")
        
        # Set the cut off date
        self._cut_off_date = cut_off_date
        self.save()

    def _is_valid_payment_date(self, payment_date: str) -> bool:
        '''
        IN: str
        OUT: bool
        Def: Permite verificar si la fecha de pago de la tarjeta de usuario es válida.
        '''
        # Verify parameter exists
        if not payment_date: raise ValueError("Payment date can't be empty")

        # Validate parameter type
        if not isinstance(payment_date, str): raise ValueError("Payment date must be a string")

        # Check if the payment date is valid
        is_correct_format = self._correct_date_format(payment_date)
        is_after_cut_off_date = self._is_payment_date_after_cut_off_date(payment_date)
        is_valid =  is_correct_format and is_after_cut_off_date
        return is_valid

    def _is_payment_date_after_cut_off_date(self, payment_date: str) -> bool:
        '''
        IN: str
        OUT: bool
        Def: Permite verificar si la fecha de pago de la tarjeta de usuario es posterior a la fecha de corte.
        '''
        # Verify parameters
        if not payment_date: raise ValueError("Payment date can't be empty")
        # Validate parameters
        if not isinstance(payment_date, str): raise ValueError("Payment date must be a string")

        # Check if the payment date is after the cut off date
        if (payment_date > str(self.get_cut_off_date())):
            return True
        else: 
            raise ValueError("The payment date must be after the cut off date")

    def _is_valid_cut_off_date(self, cut_off_date: str) -> bool:
        '''
        IN: str
        OUT: bool
        Def: Permite verificar si la fecha de corte de la tarjeta de usuario es válida.
        '''
        # Validate parameter
        if not cut_off_date: raise ValueError("Cut off date can't be empty")
        # Verify parameter type
        if not isinstance(cut_off_date, str): raise ValueError("Cut off date must be a string")
        
        # Validate the cut off date
        is_correct_format = self._correct_date_format(cut_off_date)
        is_before_payment_date = self._is_cut_off_date_before_payment_date(cut_off_date)
        is_valid = is_correct_format and is_before_payment_date
        return is_valid

    def _is_cut_off_date_before_payment_date(self, cut_off_date: str) -> bool:
        '''
        IN: str
        OUT: bool
        Def: Permite verificar si la fecha de corte de la tarjeta de usuario es anterior a la fecha de pago.
        '''
        # Validate parameter
        if not cut_off_date: raise ValueError("Cut off date can't be empty")
        # Verify parameter type
        if not isinstance(cut_off_date, str): raise ValueError("Cut off date must be a string")
        
        # Check if the cut off date is before the payment date
        if (cut_off_date < str(self._payment_date)):
            return True
        else: 
            raise ValueError("The cut off date must be before the payment date")

    def _correct_date_format(self, date: str) -> bool:
        '''
        IN: str
        OUT: bool
        Def: Permite verificar si la fecha de la tarjeta de usuario tiene el formato correcto. YYYY-MM-DD
        '''
        # Validate parameter
        if not date: raise ValueError("Date can't be empty")
        # Verify parameter type
        if not isinstance(date, str): raise ValueError("Date must be a string")
        
        # Check if the date is in the correct format: YYYY-MM-DD
        correct_pattern = re.match(r"\d{4}-\d{2}-\d{2}", date)
        
        # Revisa si el resultado es correcto, si no arroja una excepción que indica que la fecha debe tener el formato correcto
        if correct_pattern:
            return True
        else:
            raise WrongDateFormatException("The date must be in the format YYYY-MM-DD")
    
    def get_balance(self) -> float:
        '''
        IN: None
        OUT: float
        Def: Permite obtener el saldo de la tarjeta de usuario.
        '''
        return self._balance
    
    def pay(self, payment: float):
        '''
        IN: float
        OUT: None
        Def: Permite realizar un pago en la tarjeta de usuario.
        '''
        # Validate parameter
        if not payment: raise ValueError("Payment can't be empty")
        # Verify parameter
        if not self._is_correct_payment(payment): raise ValueError("Incorrect payment")

        # Apply payment
        self._balance -= payment

    def _is_correct_payment(self, payment: float) -> bool:
        '''
        IN: float
        OUT: bool
        Def: Permite verificar si el pago es correcto.
        '''
        # Validate parameter
        if not payment: raise ValueError("Payment can't be empty")
        # Verify parameter type
        if not isinstance(payment, float): raise ValueError("Payment must be a float")
        
        # Check if the payment is valid
        is_float = self._is_payment_correct_type(payment)
        is_a_significant_amount = self._is_the_payment_a_significant_amount(payment)
        not_too_big = self._is_the_payment_not_too_big(payment)
        is_valid = is_float and is_a_significant_amount and not_too_big
        return is_valid

    def _is_the_payment_not_too_big(self, payment: float) -> bool:
        '''
        IN: float
        OUT: bool
        Def: Permite verificar si el pago es menor al saldo de la tarjeta de usuario.
        '''
        # Validate parameter
        if not payment: raise ValueError("Payment can't be empty")
        # Verify parameter
        if not isinstance(payment, float): raise ValueError("Payment must be a float")
        
        # Check if the payment is less than the balance
        if payment <= self._balance:
            return True
        else:
            raise ValueError("The payment must be less than the balance")

    def _is_the_payment_a_significant_amount(self, payment: float) -> bool:
        ''' 
        IN: float
        OUT: bool
        Def: Permite verificar si el pago es una cantidad significativa.
        '''
        # Validate parameter
        if not payment: raise ValueError("Payment can't be empty")

        # Verify parameter
        if not isinstance(payment, float): raise ValueError("Payment must be a float")
        
        # Se revisa que la cantidad ingresada sea significativa y si no lo es arroja una excepción
        if payment > 0:
            return True
        else:
            raise ValueError("The payment must be a significant amount")

    def _is_payment_correct_type(self, payment: float) -> bool:
        '''
        IN: float
        OUT: bool
        Def: Permite verificar si el pago es un número flotante.
        '''
        # Validate parameter
        if not payment: raise ValueError("Payment can't be empty")
        # Verify parameter type
        if not isinstance(payment, float): raise ValueError("Payment must be a float")
        
        # Revisa si el pago es un número flotante, si no arroja una excepción que indica que el pago debe ser un número flotante
        if isinstance(payment, float):
            return True
        else:
            raise ValueError("Payment must be a float")
    
    def add_expense(self, expense: float):
        '''
        IN: float
        OUT: None
        Def: Permite agregar un gasto a la tarjeta de usuario.
        '''
        # Validate parameter
        if not expense: raise ValueError("Expense can't be empty")
        # Verify parameter
        if not isinstance(expense, float): raise ValueError("Expense must be a float")
        if not self._is_correct_expense(expense): raise ValueError("Incorrect expense")

        # Apply expense
        self._balance += expense

    def _is_correct_expense(self, expense: float) -> bool:
        '''
        IN: float
        OUT: bool
        Def: Permite verificar la cantidad ingresada como gasto es correcta.
        '''
        # Validate parameter
        if not expense: raise ValueError("Expense can't be empty")
        
        # Verify parameter type
        if not isinstance(expense, float): raise ValueError("Expense must be a float")
        
        return True
    
    def to_dict(self) -> dict:
        '''
        IN: None
        OUT: dict
        Def: Permite obtener un diccionario con los atributos de la tarjeta de usuario.'''
        return {
            "id": self.get_id(),
            "bank_card": self.get_bank_card().get_name(),  
            "bank": self.get_bank(),
            "owner_name": self.get_owner_name(),
            "payment_date": str(self.get_payment_date()),  
            "cut_off_date": str(self.get_cut_off_date()),
            "balance": self.get_balance(),
        }
    
    def get_interest(self) -> float:
        '''
        IN: None
        OUT: float
        Def: Permite obtener el interés de la tarjeta de usuario.
        '''
        return self.get_bank_card().get_interest_rate()


class Cardholder(models.Model):
    '''
    ADT: Tarjetero
    Def: Esta clase representa un tarjetero que posee el usuario. 
    Este se instancia y se asocia a un usuario en el momento de creación del usuario. 
    En el tarjetero, un usuario almacena sus tarjetas, puede agregar tarjetas, 
    obtener una o todas y como eliminar una en el momento 
    que desee dejar de poseerla. 
    El tarjetero está vacío en el momento de su creación y 
    no tiene una cantidad máxima de tarjetas definido. 
    '''
    _cards = models.ManyToManyField('UserCard', through='CardholderUserCard', related_name='cardholders')

    def add_card(self, card: UserCard):
        '''
        IN: UserCard
        OUT: None
        Def: Permite agregar una tarjeta al tarjetero.
        '''
        self._cards.add(card)

    def get_all_cards(self) -> list[UserCard]:
        '''
        IN: None
        OUT: list[UserCard]
        Def: Permite obtener todas las tarjetas del tarjetero.
        '''
        return list(self._cards.all())

    def get_card_by_name(self, name: str) -> UserCard:
        '''
        IN: str
        OUT: UserCard
        Def: Permite obtener una tarjeta del tarjetero por su nombre.
        '''
        # Verify parameter
        if not name: raise ValueError("Name can't be empty")
        
        # Validate parameter type
        if not isinstance(name, str): raise ValueError("Name must be a string")
        
        all_cards = self.get_all_cards()
        card = self._search_card_by_name(all_cards, name)
        return card
    
    def _search_card_by_name(self, all_cards:list[UserCard], name: str) -> UserCard:
        '''
        IN: list[UserCard], str
        OUT: UserCard
        Def: Permite buscar una tarjeta por su nombre en la lista de tarjetas.
        '''
        # Verify parameter
        if not all_cards: raise ValueError("Cards can't be empty")
        if not name: raise ValueError("Name can't be empty")
    
        # Validate parameter type
        if not isinstance(all_cards, list): raise ValueError("Cards must be a list")
        if not all(isinstance(card, UserCard) for card in all_cards): raise ValueError("Cards must be a list of UserCard instances")
        if not isinstance(name, str): raise ValueError("Name must be a string")
        
        # Itera la lista de todas las tarjetas hasta encontrar la tarjeta con el nombre ingresado
        for card in all_cards:
            if card.get_bank_card().get_name() == name:
                return card
        raise CardNotFoundError(name)

    def remove_card(self, card: UserCard):
        '''
        IN: UserCard
        OUT: None
        Def: Permite eliminar una tarjeta del tarjetero.
        '''
        # Verify parameter
        if not card: raise ValueError("Card can't be empty")
        # Validate parameter type
        if not isinstance(card, UserCard): raise ValueError("Card must be a UserCard")
        
        self._cards.remove(card)


# Relationship 1(cardholder) -> N(user_card)
class CardholderUserCard(models.Model):
    '''
    Esta clase no representa un ADT en términos de negocio.
    Esta clase se utiliza para definir la tabla intermedia
    entre Cardholder y UserCard, para poder migrar la relación a la base de datos
    '''
    cardholder = models.ForeignKey(Cardholder, on_delete=models.CASCADE)
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE)


class User(models.Model):
    '''
    ADT: UsuarioUsuario de la aplicación
    Def: Esta entidad representa a los usuarios de 
    la aplicación que la utilizan para fines de dominio? 
    '''
    _email = models.CharField(max_length=100, primary_key=True, null=False)
    _name = models.CharField(max_length=100, null=False)
    _password = models.CharField(max_length=100, null=False)
    _cardholder = models.OneToOneField('Cardholder', on_delete=models.CASCADE, null=True)
    
    def get_email(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el correo electrónico del usuario.
        '''
        return self._email

    def get_name(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre del usuario.
        '''
        return self._name

    def set_name(self, name: str):
        '''
        IN: str
        OUT: None
        Def: Permite establecer el nombre del usuario.
        '''
        # Verify parameter
        if not name: raise ValueError("Name can't be empty")
        
        # Validate parameter type
        if not isinstance(name, str): raise ValueError("Name must be a string")

        self._name = name

    def get_password(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la contraseña del usuario.
        '''
        return self._password

    def set_password(self, password: str):
        '''
        IN: str
        OUT: None
        Def: Permite establecer la contraseña del usuario.
        '''
        # Verify parameter
        if not password: raise ValueError("Password can't be empty")
        # Validate parameter type
        if not isinstance(password, str): raise ValueError("Password must be a string")

        self._password = password
    
    def get_cardholder(self) -> Cardholder:
        '''
        IN: None
        OUT: Cardholder
        Def: Permite obtener el tarjetero del usuario.
        '''
        return self._cardholder


class CardStatement(models.Model):
    """
    ADT: Statement de tarjeta 
    Def: “Fotografía” del estado de una tarjeta en un momento dado. 
    Se genera uno de manera automática al llegar la fecha de corte de 
    la tarjeta de usuario. Debido a que estos valores son una imágen 
    de la tarjeta en el tiempo, no son modificables y solo se proveen 
    métodos accesorios “get.”
    """
    _card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    _owner_name = models.CharField(max_length=100, null=False)
    _date = models.DateField(null=False)
    _cut_off_date = models.DateField(default=date.today, null=False)
    _payment_date = models.DateField(default=date.today, null=False)
    _debt = models.FloatField(null=False)
    _interest = models.FloatField(null=False)


    def get_card(self) -> UserCard:
        '''
        IN: None
        OUT: UserCard
        Def: Permite obtener la tarjeta de usuario asociada al estado de tarjeta.
        '''
        return self._card

    def get_owner_name(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener el nombre del propietario de la tarjeta de usuario.
        '''
        return self._owner_name

    def get_date(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la fecha del estado de tarjeta.
        '''
        return self._date
    
    def get_cut_off_date(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la fecha de corte del estado de tarjeta.
        '''
        return str(self._cut_off_date)
    
    def get_payment_date(self) -> str:
        '''
        IN: None
        OUT: str
        Def: Permite obtener la fecha de pago del estado de tarjeta.
        '''
        return str(self._payment_date)

    def get_debt(self) -> float:
        '''
        IN: None
        OUT: float
        Def: Permite obtener la deuda del estado de tarjeta.
        '''
        return self._debt

    def get_interest(self) -> float:
        return self._interest


class StatementHistory(models.Model):
    '''
    ADT: Historial de Statements de una tarjeta 
    Def: Conjunto de Statements que se han generado para una User Card. 
    Permite agregar y obtener Statements mas no borrarlos ni editarlos. 
    Esto se debe a que un Statement es una “fotografía” 
    de una tarjeta al término de un mes, 
    permitir la eliminación de uno de estos sería permitir “borrar los hechos” 
    y su edición sería permitir “cambiar la realidad”. 
    '''
    _statements = models.ManyToManyField(CardStatement, related_name='statement_histories')
    
    def get_all_statements(self) -> list[CardStatement]:
        '''
        IN: None
        OUT: list[CardStatement]
        Def: Permite obtener todos los estados de tarjeta del historial.
        '''
        return list(self._statements.all())

    def add_statement(self, statement: CardStatement):
        """
        IN: CardStatement
        OUT: None
        Def: Permite agregar un estado de tarjeta al historial.
        """
        # Verify parameter
        if not statement: raise ValueError("Statement can't be empty")
        # Validate parameter type
        if not isinstance(statement, CardStatement): raise ValueError("Statement must be a CardStatement")

        self._statements.add(statement)

