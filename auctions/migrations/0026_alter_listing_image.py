# Generated by Django 4.1.7 on 2023-04-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_alter_listing_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(null=True),
        ),
    ]