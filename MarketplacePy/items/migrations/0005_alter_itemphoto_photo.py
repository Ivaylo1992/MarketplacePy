# Generated by Django 5.1.3 on 2024-12-11 04:26

import MarketplacePy.items.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_rename_product_itemlike_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemphoto',
            name='photo',
            field=cloudinary.models.CloudinaryField(max_length=255, validators=[MarketplacePy.items.validators.FileSizeValidator(5)], verbose_name='photo'),
        ),
    ]