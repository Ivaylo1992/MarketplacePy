# Generated by Django 5.1.3 on 2024-12-18 03:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=5)),
                ('comment', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]