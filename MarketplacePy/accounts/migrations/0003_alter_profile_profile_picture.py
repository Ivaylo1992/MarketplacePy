# Generated by Django 5.1.3 on 2024-12-15 02:37

import MarketplacePy.common.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[MarketplacePy.common.validators.FileSizeValidator(5), MarketplacePy.common.validators.validate_image_content], verbose_name='profile picture'),
        ),
    ]