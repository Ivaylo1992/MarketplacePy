# Generated by Django 5.1.3 on 2024-12-10 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_itemlike'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemlike',
            old_name='product',
            new_name='item',
        ),
    ]
