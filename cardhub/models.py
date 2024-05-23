import json
import re
from django.db import models
from cardhub.exceptions.CardNotFoundError import CardNotFoundError
from cardhub.exceptions.WrongDateFormatException import WrongDateFormatException
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.utils import timezone


class BankCard(models.Model):
    _id = models.AutoField(primary_key=True)
    _bank = models.CharField(max_length=100, null=False)
    _name = models.CharField(max_length=100, null=False)
    _interest_rate = models.FloatField(null=False)
    
    def get_id(self):
        return self._id

    def get_bank(self):
        return self._bank

    def get_name(self):
        return self._name

    def get_interest_rate(self):
        return self._interest_rate


class UserCard(models.Model):
    _id = models.AutoField(primary_key=True)
    _bank_card = models.ForeignKey(BankCard, on_delete=models.CASCADE)
    _owner = models.ForeignKey('User', on_delete=models.CASCADE)
    _payment_date = models.DateField(null=False) #The format is YYYY-MM-DD
    _cut_off_date = models.DateField(null=False)
    _balance = models.FloatField(null=False)
    #_statement_history = models.OneToOneField('StatementHistory', on_delete=models.CASCADE, null=True)

    def get_id(self) -> int:
        return self._id
    
    def get_owner_name(self) -> str:
        return self._owner.get_name()
    
    def get_owner(self) -> 'User':
        return self._owner

    def get_bank_card(self) -> BankCard:
        return self._bank_card
    
    def get_name(self) -> str:
        return self._bank_card.get_name()
    
    def get_bank(self) -> str:
        return self._bank_card.get_bank()
    
    def get_payment_date(self) -> str:
        return self._payment_date
    
    def set_payment_date(self, payment_date: str):
        """Buena práctica: Validar los datos antes de asignarlos.
        # Verifica si la fecha de pago es válida antes de asignarla al atributo."""
        if not self._is_valid_payment_date(payment_date): 
            raise ValueError("Incorrect payment date")
        self._payment_date = payment_date

    def _is_valid_payment_date(self, payment_date: str) -> bool:
        """Buena práctica: Divide la validación en pasos claros.
        Verifica si la fecha es una cadena, tiene el formato correcto y es posterior a la fecha de corte."""
        is_string = self._is_date_string(payment_date) 
        is_correct_format = self._correct_date_format(payment_date)
        is_after_cut_off_date = self._is_payment_date_after_cut_off_date(payment_date)
        is_valid = is_string and is_correct_format and is_after_cut_off_date
        return is_valid

    def _is_payment_date_after_cut_off_date(self, payment_date: str) -> bool: 
        """Buena práctica: Claridad en las condiciones.
        Compara las fechas y lanza una excepción si la fecha de pago no es posterior a la fecha de corte."""
        if (payment_date > self._cut_off_date.strftime('%Y-%m-%d')):
            return True
        else: 
            raise ValueError("The payment date must be after the cut off date")
    
    def get_cut_off_date(self) -> str:
        return self._cut_off_date
    
    def set_cut_off_date(self, cut_off_date: str):
        """Buena práctica: Validar los datos antes de asignarlos.
        Verifica si la fecha de corte es válida antes de asignarla al atributo."""
        if not self._is_valid_cut_off_date(cut_off_date): raise ValueError("Incorrect cut off date")
        self._cut_off_date = cut_off_date
        
    def _is_valid_cut_off_date(self, cut_off_date: str) -> bool:
        """Buena práctica: Divide la validación en pasos claros.
        Verifica si la fecha es una cadena, tiene el formato correcto y es anterior a la fecha de pago."""
        # NO CAMBIAR EL ORDEN DE LAS SENTENCIAS PQ EXPLOTA
        is_string = self._is_date_string(cut_off_date)
        is_correct_format = self._correct_date_format(cut_off_date)
        is_before_payment_date = self._is_cut_off_date_before_payment_date(cut_off_date)
        is_valid = is_string and is_correct_format and is_before_payment_date
        return is_valid

    def _is_cut_off_date_before_payment_date(self, cut_off_date):
        """ Buena práctica: Claridad en las condiciones.
         Compara las fechas y lanza una excepción si la fecha de corte no es anterior a la fecha de pago."""
        if (cut_off_date < self._payment_date):
            return True
        else: 
            raise ValueError("The cut off date must be before the payment date")

    def _is_date_string(self, date: str) -> bool:
        """ Buena práctica: Verificar el tipo de datos.
         Verifica si la fecha es una cadena antes de continuar."""
        if (isinstance(date, str)):
            return True
        else: 
            raise ValueError("The date must be a string")
    
    def _correct_date_format(self, date: str) -> bool:
        """ Buena práctica: Uso de expresiones regulares para validar el formato de la fecha.
         Verifica si la fecha sigue el formato YYYY-MM-DD."""
        correct_pattern = re.match(r"\d{4}-\d{2}-\d{2}", date)
        if correct_pattern:
            return True
        else:
            raise WrongDateFormatException("The date must be in the format YYYY-MM-DD")
    
    def get_balance(self) -> float:
        return self._balance
    
    def pay(self, payment: float):
        """ Buena práctica: Validar los pagos antes de procesarlos.
         Verifica si el pago es válido antes de deducirlo del balance."""
        if not self._is_correct_payment(payment): raise ValueError("Incorrect payment")
        self._balance -= payment

    def _is_correct_payment(self, payment: float) -> bool:
        """ Buena práctica: Divide la validación en pasos claros.
         Verifica si el pago es un float, si es una cantidad significativa y si no excede el balance."""
        is_float = self._is_payment_correct_type(payment)
        is_a_significant_amount = self._is_the_payment_a_significant_amount(payment)
        not_too_big = self._is_the_payment_not_too_big(payment)
        is_valid = is_float and is_a_significant_amount and not_too_big
        return is_valid

    def _is_the_payment_not_too_big(self, payment):
        """ Buena práctica: Claridad en las condiciones.
         Verifica si el pago no excede el balance actual"""
        if payment <= self._balance:
            return True
        else:
            raise ValueError("The payment must be less than the balance")

    def _is_the_payment_a_significant_amount(self, payment):
        """ Buena práctica: Claridad en las condiciones.
         Verifica si el pago es una cantidad positiva."""
        if payment > 0:
            return True
        else:
            raise ValueError("The payment must be a significant amount")

    def _is_payment_correct_type(self, payment):
        """ Buena práctica: Verificar el tipo de datos.
         Verifica si el pago es un float antes de continuar."""
        if isinstance(payment, float):
            return True
        else:
            raise ValueError("Payment must be a float")

    def to_dict(self):
        """ Buena práctica: Conversión clara de un objeto a diccionario.
         Permite convertir el objeto UserCard a un diccionario de manera clara y organizada."""
        return {
            "id": self.get_id(),
            "bank_card": self.get_bank_card().get_name(),  # Modify this according to your BankCard class
            "bank": self.get_bank(),
            "owner_name": self.get_owner_name(),
            "payment_date": str(self.get_payment_date()),  # Converting date to string
            "cut_off_date": str(self.get_cut_off_date()),
            "balance": self.get_balance(),
        }


class Cardholder(models.Model):
    _cards = models.ManyToManyField('UserCard', through='CardholderUserCard', related_name='cardholders')

    def add_card(self, card: UserCard):
        """ Buena práctica: Uso de ManyToManyField para relaciones múltiples.
         Permite agregar una tarjeta al cardholder de manera eficiente."""
        self._cards.add(card)

    def get_all_cards(self) -> list[UserCard]:
        """ Buena práctica: Conversión a lista.
         Retorna todas las tarjetas como una lista, lo que facilita su manipulación."""
        return list(self._cards.all())
        return list(self._cards.all())

    def get_card_by_name(self, name: str) -> UserCard:
        all_cards = self.get_all_cards()
        card = self._search_card_by_name(all_cards, name)
        return card
    
    def _search_card_by_name(self,all_cards:list[UserCard], name: str) -> UserCard:
        """ Buena práctica: Búsqueda clara en listas.
         Itera sobre todas las tarjetas y retorna la tarjeta con el nombre correspondiente."""
        for card in all_cards:
            if card.get_bank_card().get_name() == name:
                return card
        raise CardNotFoundError(name)
        

    def remove_card(self, card: UserCard):
        """ Buena práctica: Uso de ManyToManyField para relaciones múltiples.
         Permite remover una tarjeta del cardholder de manera eficiente."""
        self._cards.remove(card)


class CardholderUserCard(models.Model):
    cardholder = models.ForeignKey(Cardholder, on_delete=models.CASCADE)
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE)


class User(models.Model):
    _email = models.CharField(max_length=100, primary_key=True, null=False)
    _name = models.CharField(max_length=100, null=False)
    _password = models.CharField(max_length=100, null=False)
    _cardholder = models.OneToOneField('Cardholder', on_delete=models.CASCADE, null=True)
    
    def get_email(self):
        return self._email

    def get_name(self):
        return self._name

    def set_name(self, name):
        """Buena práctica: Verificar el tipo de datos
        antes de asignar el valor."""
        if not isinstance(name, str): raise ValueError("Name must be a string")
        self._name = name

    def get_password(self):
        return self._password

    def set_password(self, password):
        """Buena práctica: Verificar el tipo de datos
        antes de asignar el valor."""
        if not isinstance(password, str): raise ValueError("Password must be a string")
        self._password = password
    
    def get_cardholder(self) -> Cardholder:
        return self._cardholder


class CardStatement(models.Model):
    _card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    _owner_name = models.CharField(max_length=100, null=False)
    _date = models.DateField(null=False)
    _debt = models.FloatField(null=False)
    _interest = models.FloatField(null=False)


    def get_card(self) -> UserCard:
        return self._card

    def get_owner_name(self) -> str:
        return self._owner_name

    def get_date(self) -> str:
        return self._date

    def get_debt(self) -> float:
        return self._debt

    def get_interest(self) -> float:
        return self._interest


class StatementHistory(models.Model):
    _statements = models.ManyToManyField(CardStatement, related_name='statement_histories')
    

    def get_all_statements(self) -> list[CardStatement]:
        return list(self._statements.all())

    def add_statement(self, statement: CardStatement):
        if not isinstance(statement, CardStatement): raise ValueError("Statement must be a CardStatement")
        self._statements.add(statement)
        

class AccountStatement(models.Model):
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_debt = models.FloatField(default=0.0)
    total_payments = models.FloatField(default=0.0)

    def add_payment(self, payment):
        if not isinstance(payment, (float, int)):
            raise TypeError("El pago debe ser un número")
        if payment > self.total_debt:
            raise ValueError("El pago no puede ser mayor que la deuda pendiente")
        self.total_payments += payment
        self.total_debt -= payment
        self.save()
    
    def add_charge(self, amount):
        if not isinstance(amount, (float, int)):
            raise TypeError("El monto debe ser un número")
        self.total_debt += amount
        self.save()

    def __str__(self):
        return f"Statement for {self.card.get_name()} on {self.date}"
