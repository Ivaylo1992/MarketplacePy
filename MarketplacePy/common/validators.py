from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image


@deconstructible
class FileSizeValidator:
    def __init__(self, file_size_mb, message=None):
        self.file_size_mb = file_size_mb
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"File size must not exceed {self.file_size_mb}MB"
        else:
            self.__message = value

    def __call__(self, value):
        if value.size > self.file_size_mb * 1024 * 1024:
            raise ValidationError(self.message)


def validate_image_content(file):
    try:
        # Open the file to verify its content
        img = Image.open(file)
        img.verify()  # Verify that it is, indeed, an image
    except (IOError, SyntaxError):
        raise ValidationError("The uploaded file is not a valid image.")
