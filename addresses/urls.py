from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('addresses/', views.AddressView.as_view(), name='addresses-view'),
    path('addresses/delete/<int:pk>/', views.AddressDeleteView.as_view(), name="addresses-delete-view"),
    path('addresses/update/<int:pk>/', views.AddressUpdateView.as_view(), name="addresses-update-view"),
    path('addresses/default/<int:pk>/', views.AddressDefaultView.as_view(), name="addresses-default-view"),
    path('addresses/store-delivery/', views.DeliveryStoreView.as_view(), name="addresses-store-delivery-view"),

]
