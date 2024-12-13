from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('store/', views.StoreView.as_view(), name='store-view'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('variant/<int:pk>', views.product_variants_choice, name='choice-variant-view'),
    path('search/', views.search_products, name='search-products'),
    # path('api/categories/', api_views.CategoryListView.as_view(), name='categories-list-api'),
    # path('api/categories/create/', api_views.CategoryCreateView.as_view(), name='categories-create-api'),
    # path('api/categories/update/<int:pk>/', api_views.CategoryUpdateView.as_view(), name='categories-update-api'),
    # path('api/categories/delete/<int:pk>/', api_views.CategoryDeleteView.as_view(), name='categories-delete-api'),
    # path('api/categories/<int:pk>/', api_views.CategoryRetrieveView.as_view(), name='categories-retrieve-api'),
    # path('api/products/', api_views.ProductListView.as_view(), name='products-list-api'),
    # path('api/products/create/', api_views.ProductCreateView.as_view(), name='products-create-api'),
    # path('api/products/update/<int:pk>/', api_views.ProductUpdateView.as_view(), name='products-update-api'),
    # path('api/products/delete/<int:pk>/', api_views.ProductDeleteView.as_view(), name='products-delete-api'),
    # path('api/products/<int:pk>/', api_views.ProductRetrieveView.as_view(), name='products-retrieve-api'),
    # path('api/products-variant/create/', api_views.ProductVariantCreateView.as_view(), name='products-variant-create-api'),
    # path('api/products-variant/delete/<int:pk>/', api_views.ProductVariantDeleteView.as_view(), name='products-variant-delete-api'),
    # path('api/products-variant/update/<int:pk>/', api_views.ProductVariantUpdateView.as_view(), name='products-variant-update-api'),
]
