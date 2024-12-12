from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models

from MarketplacePy.common.models import TimeStampedMixin, HasUser
from MarketplacePy.items.validators import FileSizeValidator


class Category(TimeStampedMixin):
    CATEGORY_NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=CATEGORY_NAME_MAX_LENGTH,
        unique=True,
        null=False,
        blank=False,
    )

    category_image = CloudinaryField(
        'category_image',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(TimeStampedMixin, HasUser):
    NAME_MAX_LENGTH = 100
    NAME_MIN_LENGTH = 2
    DESCRIPTION_MAX_LENGTH = 500
    DESCRIPTION_MIN_LENGTH = 100
    PRICE_MAX_VALUE = 9999.00
    PRICE_MIN_VALUE = 0.00

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(NAME_MIN_LENGTH),
        ]
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(DESCRIPTION_MIN_LENGTH),
        ]
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        validators=[
            MinValueValidator(PRICE_MIN_VALUE),
            MaxValueValidator(PRICE_MAX_VALUE)
        ]
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='items',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ItemPhoto(TimeStampedMixin, HasUser):
    MAX_PHOTO_SIZE_MB = 5
    MAX_PHOTOS = 10
    photo = CloudinaryField(
        "photo",
        null=False,
        blank=False,
        validators=[
            FileSizeValidator(MAX_PHOTO_SIZE_MB),
        ]
    )

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='photos',
    )

    class Meta:
        verbose_name_plural = 'Photos'
        ordering = ['-created_at']

    def clean(self):
        if self.item.photos.count() >= self.MAX_PHOTOS:
            raise ValidationError(f"A product can have a maximum of {self.MAX_PHOTOS} photos.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ItemLike(HasUser, TimeStampedMixin):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="likes"
    )
