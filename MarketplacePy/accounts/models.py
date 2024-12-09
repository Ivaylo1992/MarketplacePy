from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model

from MarketplacePy.accounts.managers import AppUserManager
from MarketplacePy.accounts.validators import FirstCapitalValidator


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    last_login = models.DateTimeField(
        auto_now=True
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.email


UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30
    LOCATION_MAX_LENGTH = 20

    user = models.OneToOneField(
        to=UserModel,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            FirstCapitalValidator()
        ]
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            FirstCapitalValidator()
        ],
    )

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        blank=True,
        null=True,
    )

    profile_picture = CloudinaryField(
        'profile picture',
        blank=True,
        null=True,
    )

    def get_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        return self.user.email
