"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView
from azbankgateways.urls import az_bank_gateways_urls

admin.site.site_header = 'پنل مدیریت تهران بوتیک'
admin.site.index_title = 'پنل مدیریت فروشگاه'
admin.site.site_title = 'صفحه مدیریت تهران بوتیک'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('', include('accounts.urls', namespace="accounts")),
    path('', include('medias.urls', namespace="medias")),
    path('', include('products.urls', namespace="products")),
    path('', include('addresses.urls', namespace="addresses")),
    path('', include('carts.urls', namespace="carts")),
    path('', include('orders.urls', namespace="orders")),
    path("bankgateways/", az_bank_gateways_urls()),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
