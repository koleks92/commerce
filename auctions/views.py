from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Listing

class CreateFroms(forms.Form):
    # Categories from models.listing
    CHOICES = Listing.CATEGORIES

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter name of the item'}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'placeholder': 'Enter description of the item'}))
    price = forms.CharField(label="Price", widget=forms.TextInput(attrs={'placeholder': 'Enter price of the item'}))
    category = forms.ChoiceField(widget=forms.Select, required=False, choices=CHOICES, initial=False)
    image = forms.URLField(required=False)
                                                                                                                                                           
                                                                   


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create(request):
    if request.method == "POST":
        print(request.POST["category"])
        l_name = request.POST["name"]
        l_description = request.POST["description"]
        l_price = request.POST["price"]
        if request.POST["category"]:
            l_category = request.POST["category"]
        else:
            l_category = None
        if request.POST["image"]:
            l_image = request.POST["image"]
        else:
            l_image = False


        l = Listing(name=l_name, description=l_description, price=l_price, category=l_category, image=l_image, user=request.user)
        l.save()

        return HttpResponseRedirect(reverse("index"))




    return render(request, "auctions/create.html", {
        "create": CreateFroms()
    })
