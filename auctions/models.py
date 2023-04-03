from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
    ('', 'Choose Category'),
    ('electornics', 'Electronics'),
    ('motors', 'Motors'),
    ('fashion', 'Fashion'),
    ('collectibles', 'Collectibles and Art'),
    ('sports', 'Sports'),
    ('health', 'Health and Beauty'),
    ('industrial', 'Industrial Equipment'),
    ('home', 'Home and Garden')
]

    name = models.CharField(max_length=64)                                                  #name
    description = models.CharField(max_length=640, null=True)                               #description
    price = models.DecimalField(max_digits=20, decimal_places=2)                            #price
    date = models.DateTimeField(auto_now_add=True)                                          #date creation
    image = models.URLField(max_length=200, null=True, blank=True)                                                 #image                                                         #image
    category = models.CharField(max_length=64, choices=CATEGORIES, null=True, blank=True)                          #category
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")           #user

    def __str__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                            # user
    date = models.DateTimeField(auto_now=True)                                                          # date bid
    bid = models.DecimalField(max_digits=20, decimal_places=2, default=0)                               # user bid
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing", default=0)   # listing
    pass

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment", default=0)      # listing                      # item
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User", default=0)            # user
    date = models.DateTimeField(auto_now=True)                                                          # date comment
    comment = models.CharField(max_length=128, default="")                                              # comments
    pass