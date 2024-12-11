from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryList.as_view(), name="gallery"),
    path('create/', views.GalleryCreate.as_view(), name="gallery_create"),
    path('<int:pk>/', views.GalleryDetail.as_view(), name="gallery_detail"),
    path('<int:pk>/update/', views.GalleryUpdate.as_view(), name="gallery_update"),
    
]
