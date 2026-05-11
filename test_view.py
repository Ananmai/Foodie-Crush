import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_api.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from core.models import User
from recipe.views import PaymentView

factory = APIRequestFactory()
user = User.objects.first()
if not user:
    user = User.objects.create(email='test@example.com', name='Test User')

items = [{'id': 'a2', 'title': 'Farmhouse Pizza', 'price': '249', 'img': '...', 'qty': 3}]
request = factory.post('/api/recipe/payment/', data=json.dumps({'items': items}), content_type='application/json')
force_authenticate(request, user=user)

view = PaymentView.as_view()
response = view(request)

print(response.status_code)
print(response.data)
