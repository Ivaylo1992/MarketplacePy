from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class FirstCapitalValidator:
    """
    Validates that the first character of a string is uppercase.
    """

    def __init__(self, message=None):
        self.message = message
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        if not value:
            self.__message = "Name must start with a capital letter"
        else:
            self.__message = value

    def __call__(self, value):
        if not value.istitle():
            raise ValidationError(self.message)