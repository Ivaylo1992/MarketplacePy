from cloudinary.exceptions import Error
from django.core.exceptions import ValidationError

from django import forms

from MarketplacePy.common.forms import MultipleImageField
from MarketplacePy.items.models import Item, ItemPhoto


class PriceRangeForm(forms.Form):
    min_price = forms.DecimalField(
        initial=0,
        min_value=0,
        label="Minimum Price",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    max_price = forms.DecimalField(
        initial=9999,
        max_value=9999,
        label="Maximum Price",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control", })
    )


class ItemAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'category']


class ItemPhotoAddForm(forms.Form):
    photo = MultipleImageField()

    def save_photos(self, user, item):
        photos = self.files.getlist('photo')
        photo_instances = []

        for photo in photos:

            photo_instance = ItemPhoto(
                photo=photo,
                user=user,
                item=item,
            )
            try:
                photo_instance.full_clean()
                photo_instance.save()
                photo_instances.append(photo_instance)
            except ValidationError as e:
                self.add_error(None, e.message_dict)
            except Error:
                self.add_error(None, "Error uploading photo to Cloudinary.")

        return photo_instances


class ItemPhotoEditForm(ItemPhotoAddForm):
    photo = MultipleImageField(required=False)


class SearchItemForm(forms.Form):
    query_param = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search for products..."
        })
    )
