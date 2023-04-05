from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Listing, Bid, Comment
from django.db.models import Max

class CreateForms(forms.Form):
    # Categories from models.listing
    CHOICES = Listing.CATEGORIES

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter name of the item'}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'placeholder': 'Enter description of the item'}))
    price = forms.CharField(label="Price", widget=forms.TextInput(attrs={'placeholder': 'Enter price of the item'}))
    category = forms.ChoiceField(widget=forms.Select, required=False, choices=CHOICES, initial=False)
    image = forms.URLField(required=False)

                                                                                                            

''' Views functions '''                     

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
        "create": CreateForms()
    })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        watchlist = listing.watchlist.all()
        bids = Bid.objects.filter(listing_id=listing)
        comments = Comment.objects.filter(listing_id=listing).order_by('-date')     # Get comments and order by newest first

        listing_user = False
        if request.user == listing.user:                                            # Check if logged in user is one who created listing
            listing_user = True

        w = False
        if request.user in watchlist:                                               # Check if logged in user in watchlist 
            w = True

        bc = False                                                      
        if request.user.is_authenticated:                                           # Check if user logged in, if so turn on bids/comments
            bc = True 
        
        active = True                                                               # Check if listing is active
        if listing.active == False:
            active = False

        if bids:
            num_bids = len(bids)                                                    # Get number of bids
            max_bid = bids.order_by('-bid')[0]                                      # Get highest bid
            highest_user = False
            if request.user == max_bid.user:                                        # Check if logged in user is one with highest bid
                highest_user = True
        


        return render(request, "auctions/listing.html", {
            "listing": listing,
            "w": w,                                         # If user in Watchlist
            "bc": bc,                                       # Bids/Comments
            "listing_user": listing_user,                   # User = Listing User
            "num_bids": num_bids,                           # Number of bids
            "highest_user": highest_user,                   # Highest bid user
            "active": active,                               # Active listing 
            "comments": comments                            # Comments
            })

    except:
        return render(request, "auctions/error.html", {
        "message" : "Listing does't exist"
        })

@login_required
def add_watchlist(request, listing_id):
    try:
        if request.method == "POST":
            listing = Listing.objects.get(id=listing_id)
            if request.POST['watchlist'] == 'Add':                                          # Add user to listing watchlist
                listing.watchlist.add(request.user)
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
            elif request.POST['watchlist'] == 'Remove':                                     # Remove user from listing watchlist
                listing.watchlist.remove(request.user)
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

    except:                                                                                 # Error check
        return render(request, "auctions/error.html", {
        "message" : "Something went wrong ! Please try again."
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
            
            if listing.active == False:
                return render(request, "auctions/error.html", {
                "message" : "You can't bid on closed listing"
                })

            
            if len(bids) == 0:                                                                  # If first bid !
                if float(bid) < listing.price:
                    return render(request, "auctions/error.html", {
                    "message" : "You need to bid higher or the same number than actual price"
                    })
            if len(bids) > 0:                                                                   # If not first bid
                if float(bid) <= listing.price:
                    return render(request, "auctions/error.html", {
                    "message" : "You need to bid higher number than actual price"
                    })

            try:
                b = Bid(user = request.user, bid = float(bid), listing_id = listing).save()     # Create bid
                listing.price = float(bid)                                                      # Change listing price !
                listing.save()                                                                  # Save listing price
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
            except:
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

        except:
            return render(request, "auctions/error.html", {
            "message" : "Something went wrong ! Please try again."
            })
        
@login_required
def close(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            if listing.user != request.user:                                                        # Double check if logged in user is correct user
                return render(request, "auctions/error.html", {
                "message" : "You can't close the listing you did't create."
                })
            
            if listing.active == True:                                                              # Change listing bool for active
                listing.active = False
            else:
                listing.active = True
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        except:
            return render(request, "auctions/error.html", {
            "message" : "Something went wrong ! Please try again."
            })

        
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            comment = request.POST['comment']                                                   # Get comment
            c = Comment(listing_id = listing, user = request.user, comment = comment)           # Create instance of Comment
            c.save()                                                                            # Save
            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        except:
            return render(request, "auctions/error.html", {
            "message" : "Something went wrong ! Please try again."
            })
        
@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlist = request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(watchlist = request.user)
    })

def categories(request):
    categories = Listing.CATEGORIES[1:]
    return render(request, "auctions/categories.html", {
    "categories": categories
    })

def category(request, category_name):
    try:
        category = Listing.objects.get(category = category_name).get_category_display()
        return render(request, "auctions/category.html", {
            "listings": Listing.objects.filter(category = category_name),
            "category": category
            })
    except:
        return render(request, "auctions/error.html", {
            "message" : "There are no listings in that category yet"
            })
        

    



        



        




    



    