from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path('orders/', views.CreateOrderView.as_view(), name="create-order"),
    path('orders/list/pdf/', views.GenerateOrderPDF.as_view(), name='orders-list-pdf'),
    path('checkout/', views.CheckoutView.as_view(), name="checkout-view"),
    path('callback/', views.callback, name="callback-view")
]
