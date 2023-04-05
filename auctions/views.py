from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Listing, Bid
from django.db.models import Max

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

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        watchlist = listing.watchlist.all()
        bids = Bid.objects.filter(listing_id=listing)

        active = True
        if request.user == listing.user:            # Check if logged in user is one who created listing
            active = False
        
        if bids:
            num_bids = len(bids)                        # Get number of bids
            max_bid = bids.order_by('-bid')[0]          # Get highest bid
            user = False
            if request.user == max_bid.user:            # Check if logged in user is one with highest bid
                user = True
            num_user = (num_bids, user, active)
        else:
            num_user = (0,False, active)                  # (Number of bids, User is not highet bidder, Biding is active)



        if request.user.is_authenticated == False:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bc": False,                               # Bids/Comments
                "num_bids": num_bids                       # Number of bids
            })
        
        if request.user in watchlist:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "w": True,                                 # Already in Watchlist
                "bc": num_user                             # Turn on bids/comments, (Number of bids, User, Active)
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "no_w": True,                              # Not in Watchlist
                "bc": num_user                             # Turn on bids/comments, (Number of bids, User, Active)
                })
    except:
        return render(request, "auctions/error.html", {
        "message" : "Listing does't exists"
        })

@login_required
def watchlist(request, listing_id):
    try:
        if request.method == "POST":
            listing = Listing.objects.get(id=listing_id)
            if request.POST['watchlist'] == 'Add':
                listing.watchlist.add(request.user)
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
            elif request.POST['watchlist'] == 'Remove':
                listing.watchlist.remove(request.user)
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

    except:
        return render(request, "auctions/error.html", {
        "message" : "You need to be logged in to add to 'Watchlist'"
        })
    
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        try:
            bid = request.POST['bid']
            listing = Listing.objects.get(id=listing_id)
            bids = Bid.objects.filter(listing_id=listing)


            if request.user == listing.user:                                                    # If trying to bid on own listing
                return render(request, "auctions/error.html", {
                "message" : "You can't bid on your own listing"
                })
            
            if len(bids) == 0:                                                                      # If first bid !
                if float(bid) < listing.price:
                    return render(request, "auctions/error.html", {
                    "message" : "You need to bid higher number than actual price"
                    })
            if len(bids) > 0:                                                                    # If not first bid
                if float(bid) <= listing.price:
                    return render(request, "auctions/error.html", {
                    "message" : "You need to bid higher number than actual price"
                    })
                                      
            try:
                b = Bid(user = request.user, bid = float(bid), listing_id = listing).save()  # Create bid
                listing.price = float(bid)                                                   # Change listing price !
                listing.save()                                                               # Save listing price
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
            except:
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

        except:
            return render(request, "auctions/error.html", {
            "message" : "Something went wrong ! Please try again."
            })



        




    



    