from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from products.api.serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from products.filters import ProductFilter
from products.models import Category, Product, ProductVariant
from rest_framework import filters


# Create your views here.
class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class CategoryRetrieveView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class ProductListView(ListAPIView):
    queryset = Product.objects.filter(published=True)
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class ProductVariantCreateView(CreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class ProductVariantDeleteView(DestroyAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class ProductVariantUpdateView(UpdateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
