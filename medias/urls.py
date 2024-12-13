from django.urls import path
from medias import views

app_name = "medias"
urlpatterns = [
    path('medias/', views.ImageListView.as_view(), name="medias-list"),
    path('medias/create/', views.ImageCreateView.as_view(), name="medias-create"),
    path('medias/delete/<int:pk>/', views.ImageDeleteView.as_view(), name="medias-delete"),
    path('medias/update/<int:pk>/', views.ImageUpdateView.as_view(), name="medias-update"),
    path('medias/<int:pk>/', views.ImageRetrieveView.as_view(), name="medias-retrieve"),
]
