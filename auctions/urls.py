from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<str:category_name>", views.category, name="category"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
]
