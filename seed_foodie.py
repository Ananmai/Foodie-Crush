import os
import sys
import django
import urllib.request
from django.core.files.base import ContentFile

sys.path.append(r'C:\Users\Dell\Desktop\new')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_api.settings')
django.setup()

from core.models import User, Restaurant, Recipe, Tag, Ingredient

# Clear existing data
Restaurant.objects.all().delete()
Recipe.objects.all().delete()

# Get the admin user
admin_user = User.objects.filter(email='admin@example.com').first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin@example.com', 'admin123')

def save_image_from_url(model_instance, url, filename):
    try:
        response = urllib.request.urlopen(url)
        model_instance.image.save(filename, ContentFile(response.read()), save=True)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# High Quality Restaurants
r1 = Restaurant.objects.create(
    user=admin_user, name="The Crimson Plate", description="Fine dining with a modern twist.", address="123 Culinary Ave, New York, NY"
)
save_image_from_url(r1, "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=600", "crimson.jpg")

r2 = Restaurant.objects.create(
    user=admin_user, name="Sushi Sakura", description="Authentic Japanese Sushi & Ramen.", address="45 Tokyo Street, San Francisco, CA"
)
save_image_from_url(r2, "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=600", "sushi.jpg")

r3 = Restaurant.objects.create(
    user=admin_user, name="Mama's Italian", description="Handcrafted pasta and wood-fired pizzas.", address="88 Napoli Road, Chicago, IL"
)
save_image_from_url(r3, "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600", "italian.jpg")

# Recipes for The Crimson Plate
rc1 = Recipe.objects.create(user=admin_user, restaurant=r1, title="Truffle Beef Wellington", description="Tender beef tenderloin coated in mushroom duxelles.", time_minutes=45, price=45.99)
save_image_from_url(rc1, "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=500", "beef.jpg")

rc2 = Recipe.objects.create(user=admin_user, restaurant=r1, title="Pan-Seared Scallops", description="Jumbo scallops with a sweet corn puree and crispy pancetta.", time_minutes=20, price=28.50)
save_image_from_url(rc2, "https://images.unsplash.com/photo-1599084990807-684d00874e01?w=500", "scallops.jpg")

# Recipes for Sushi Sakura
rc3 = Recipe.objects.create(user=admin_user, restaurant=r2, title="Dragon Roll", description="Eel and cucumber roll topped with avocado and sweet eel sauce.", time_minutes=15, price=18.00)
save_image_from_url(rc3, "https://images.unsplash.com/photo-1553621042-f6e147245754?w=500", "roll.jpg")

rc4 = Recipe.objects.create(user=admin_user, restaurant=r2, title="Spicy Tonkotsu Ramen", description="Rich pork broth served with chashu, soft boiled egg, and fresh scallions.", time_minutes=30, price=16.50)
save_image_from_url(rc4, "https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=500", "ramen.jpg")

# Recipes for Mama's Italian
rc5 = Recipe.objects.create(user=admin_user, restaurant=r3, title="Margherita Pizza", description="Classic Neapolitan pizza with San Marzano tomatoes, fresh mozzarella, and basil.", time_minutes=25, price=14.99)
save_image_from_url(rc5, "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500", "pizza.jpg")

rc6 = Recipe.objects.create(user=admin_user, restaurant=r3, title="Fettuccine Alfredo", description="Fresh pasta tossed in a rich, creamy parmesan and butter sauce.", time_minutes=20, price=16.99)
save_image_from_url(rc6, "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=500", "pasta.jpg")

print("Database populated WITH properly downloaded images!")
