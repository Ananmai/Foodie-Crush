from django.shortcuts import render, redirect
from .models import Restaurant, Item, Customer, Cart

def index(request):
    return render(request, "delivery/index.html", {"restaurants": Restaurant.objects.all()})

def restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk = restaurant_id)
    return render(request, "delivery/restaurant.html", {"restaurant": restaurant, "items": restaurant.items.all()})

def add_to_cart(request, item_id):
    item = Item.objects.get(pk = item_id)
    customer = Customer.objects.first()
    if customer:
        cart, created = Cart.objects.get_or_create(customer = customer)
        cart.items.add(item)
    return redirect("restaurant", restaurant_id = item.restaurant.id)

def cart(request):
    customer = Customer.objects.first()
    if customer:
        cart, created = Cart.objects.get_or_create(customer = customer)
        return render(request, "delivery/cart.html", {"cart": cart, "items": cart.items.all(), "total_price": cart.total_price()})
    return redirect("index")

def checkout(request):
    customer = Customer.objects.first()
    if customer:
        cart, created = Cart.objects.get_or_create(customer = customer)
        return render(request, "delivery/checkout.html", {"total_price": cart.total_price()})
    return redirect("index")
