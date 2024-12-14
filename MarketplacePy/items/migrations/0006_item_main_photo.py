# Generated by Django 5.1.3 on 2024-12-13 03:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_alter_itemphoto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='main_photo',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='item_main_photo'),
            preserve_default=False,
        ),
    ]