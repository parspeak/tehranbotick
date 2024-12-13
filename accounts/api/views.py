from accounts.api.serializers import UserSerializer, UserCreateUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.api.mixins import UserPasswordUpdateMixin
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from accounts.models import User


# admin panel user list
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )


# admin panel retrieve user
class UserRetrieveView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


# admin panel delete user
class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


# admin panel update user
class UserUpdateView(UserPasswordUpdateMixin, UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class UserRegisterView(CreateAPIView):
    serializer_class = UserCreateUpdateSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        User.objects.create_user(
            phone_number=validated_data.get('phone_number'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )


class UserEditView(UserPasswordUpdateMixin, UpdateAPIView):
    serializer_class = UserCreateUpdateSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)
