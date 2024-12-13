from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.api import views as api_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='user-login-view'),
    path('login/verify/', views.VerifyLogin.as_view(), name='user-login-verify-view'),
    path('logout/', views.logout_view, name='user-logout-view'),

    path('profile/account-detail/', views.ProfileDetailView.as_view(), name="user-profile-detail"),
    path('profile/orders-detail/', views.ProfileOrdersView.as_view(), name="user-profile-orders"),

    path('signup/', views.SignupView.as_view(), name="user-signup-view"),
    path('signup/verify/', views.VerifySignup.as_view(), name='user-signup-verify-view'),

    path('api/users/', api_views.UserListView.as_view(), name='user-list-api'),
    path('api/users/<int:pk>/', api_views.UserRetrieveView.as_view(), name='user-retrieve-api'),
    path('api/users/delete/<int:pk>/', api_views.UserDeleteView.as_view(), name='user-delete-api'),
    path('api/users/update/<int:pk>/', api_views.UserUpdateView.as_view(), name='user-update-api'),
    path('api/users/update/', api_views.UserEditView.as_view(), name='user-update-profile-api'),
    path('api/register/', api_views.UserRegisterView.as_view(), name='user-register-api'),
    path('api/login/', TokenObtainPairView.as_view(), name='user-login-api'),

]