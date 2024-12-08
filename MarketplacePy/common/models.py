from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HasUser(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.RESTRICT,
    )

    class Meta:
        abstract = True
