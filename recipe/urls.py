from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('restaurants', views.RestaurantViewSet)
router.register('cart', views.CartViewSet)
router.register('orders', views.OrderViewSet)

app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls)),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment-success'),
]
