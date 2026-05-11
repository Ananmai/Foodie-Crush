import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_api.settings')
django.setup()

from core.models import User, Cart, CartItem, Recipe, Order
from decimal import Decimal

user = User.objects.first()
if not user:
    user = User.objects.create(email='test@example.com', name='Test User')
cart, _ = Cart.objects.get_or_create(user=user)

items = [{'id': 'a2', 'title': 'Farmhouse Pizza', 'price': '249', 'img': '...', 'qty': 3}]

CartItem.objects.filter(cart=cart).delete()
for item in items:
    try:
        recipe = Recipe.objects.get(id=item.get('id'))
        CartItem.objects.create(cart=cart, recipe=recipe, quantity=1)
    except (Recipe.DoesNotExist, ValueError):
        continue

total_amount = int(cart.total_price * 100)
if total_amount == 0:
    total_amount = int(sum([float(item.get('price', 0)) * int(item.get('qty', 1)) for item in items]) * 100)
    if total_amount > 0:
        delivery = 3000
        tax = int(total_amount * 0.05)
        total_amount += (delivery + tax)

import uuid
razorpay_order_id = f"order_mock_{uuid.uuid4().hex[:10]}"

try:
    total_for_order = cart.total_price
    print("total_for_order type:", type(total_for_order), "value:", total_for_order)
    Order.objects.create(user=user, items=items, total_amount=total_for_order, razorpay_order_id=razorpay_order_id, status='PENDING')
    print("Success! Order created.")
except Exception as e:
    print("Error:", type(e), e)
