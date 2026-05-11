import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_api.settings')
django.setup()

import razorpay
from django.conf import settings

rzp_key = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_dummy')
rzp_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'dummy_secret')

client = razorpay.Client(auth=(rzp_key, rzp_secret))
try:
    total_amount = 81435
    razorpay_order = client.order.create(data={"amount": total_amount, "currency": "INR", "receipt": "order_1"})
    print("Success!", razorpay_order['id'])
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error:", str(e))
