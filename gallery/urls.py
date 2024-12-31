from django.urls import path
from . import views
from .views import ConvertWebpView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'gallery'

urlpatterns = [
    path('search/<str:q>/', views.GallerySearch.as_view(), name='gallery_search'),
    path('category/<str:slug>/', views.GalleryListByCategory.as_view(), name='gallery_list_by_category'),
    path('<int:pk>/update/', views.GalleryUpdate.as_view(), name='gallery_update'),
    path('<int:pk>/', views.GalleryDetail.as_view(), name='gallery_detail'),
    path('create/', views.GalleryCreate.as_view(), name='gallery_create'),
    path('webp/', ConvertWebpView.as_view(), name='webp'),
    path('', views.GalleryList.as_view(), name='gallery_list'),
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)