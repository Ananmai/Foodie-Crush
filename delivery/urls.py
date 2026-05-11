from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/<int:restaurant_id>", views.restaurant, name="restaurant"),
    path("cart", views.cart, name="cart"),
]
