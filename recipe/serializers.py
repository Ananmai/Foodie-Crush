from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient, Restaurant, Cart, CartItem, Order

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address', 'image']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients', 'restaurant', 'restaurant_name']
        read_only_fields = ['id']

class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']

class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}

class CartItemSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), source='recipe', write_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'recipe', 'recipe_id', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'items', 'total_amount', 'razorpay_order_id', 'razorpay_payment_id', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
