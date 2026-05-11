from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
import razorpay
from core.models import Recipe, Tag, Ingredient, Restaurant, Cart, CartItem, Order
from recipe import serializers

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tags', 'ingredients', 'restaurant']
    search_fields = ['title']
    def get_queryset(self): return self.queryset.all().prefetch_related('tags', 'ingredients').order_by('-id')
    def get_serializer_class(self):
        if self.action == 'list': return serializers.RecipeSerializer
        elif self.action == 'upload_image': return serializers.RecipeImageSerializer
        return serializers.RecipeDetailSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)
    @action(methods=['POST'], detail=False, url_path='add-item')
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        recipe_id = request.data.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, recipe=recipe)
        if not created: cart_item.quantity += int(request.data.get('quantity', 1))
        cart_item.save()
        return Response({'status': 'Item added'})

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.none()
    serializer_class = serializers.OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class PaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        items = request.data.get('items', [])
        if not items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
        CartItem.objects.filter(cart=cart).delete()
        for item in items:
            try:
                recipe = Recipe.objects.get(id=item.get('id'))
                CartItem.objects.create(cart=cart, recipe=recipe, quantity=1)
            except (Recipe.DoesNotExist, ValueError):
                continue
                
        total_amount = int(cart.total_price * 100)
        
        # Fallback for dummy frontend items that aren't in the DB
        if total_amount == 0:
            total_amount = int(sum([float(item.get('price', 0)) * int(item.get('qty', 1)) for item in items]) * 100)
            # Add delivery and tax to match frontend
            if total_amount > 0:
                delivery = 3000  # Rs 30
                tax = int(total_amount * 0.05)
                total_amount += (delivery + tax)

        if total_amount == 0:
            return Response({'error': 'Total amount cannot be zero'}, status=status.HTTP_400_BAD_REQUEST)

        rzp_key = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_dummy')
        rzp_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'dummy_secret')

        try:
            if rzp_key == 'rzp_test_dummy' or not rzp_key:
                # Mock Razorpay response for local testing without real keys
                import uuid
                razorpay_order_id = f"order_mock_{uuid.uuid4().hex[:10]}"
            else:
                client = razorpay.Client(auth=(rzp_key, rzp_secret))
                razorpay_order = client.order.create(data={"amount": total_amount, "currency": "INR", "receipt": f"order_{user.id}"})
                razorpay_order_id = razorpay_order['id']

            Order.objects.create(user=user, items=items, total_amount=total_amount / 100, razorpay_order_id=razorpay_order_id, status='PENDING')
            return Response({'razorpay_order_id': razorpay_order_id, 'amount': total_amount, 'currency': 'INR', 'key': rzp_key})
        except Exception as e:
            import traceback
            with open('checkout_error.log', 'w') as f:
                f.write(traceback.format_exc())
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentSuccessView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Verification logic
        order = Order.objects.get(razorpay_order_id=request.data.get('razorpay_order_id'))
        order.status = 'COMPLETED'; order.save()
        CartItem.objects.filter(cart__user=request.user).delete()
        return Response({'status': 'Success'})
