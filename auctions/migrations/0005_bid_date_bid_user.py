# Generated by Django 4.1.7 on 2023-03-30 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
