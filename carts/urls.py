from django.urls import path
from carts import views

app_name = "carts"
urlpatterns = [
    path('carts/promocode/', views.PromoCodeView.as_view(), name='promo-view'),
    path('carts/<int:pk>/', views.CartView.as_view(), name='cart-view'),
    path('carts/', views.CartView.as_view(), name='list-cart-view'),
]
