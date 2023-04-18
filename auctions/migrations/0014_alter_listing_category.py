# Generated by Django 4.1.7 on 2023-04-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_category_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('', 'Choose Category'), ('electornics', 'Electronics'), ('motors', 'Motors'), ('fashion', 'Fashion'), ('collectibles', 'Collectibles and Art'), ('sports', 'Sports'), ('health', 'Health and Beauty'), ('industrial', 'Industrial Equipment'), ('home', 'Home and Garden')], max_length=64, null=True),
        ),
    ]