from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'gallery'

urlpatterns = [
    path('search/<str:q>/', views.GallerySearch.as_view()),
    path('category/<str:slug>/', views.GalleryListByCategory.as_view(), name='gallery_list_by_category'),    
    path('<int:pk>/update/', views.GalleryUpdate.as_view()),
    path('<int:pk>/', views.GalleryDetail.as_view()),
    path('create/', views.GalleryCreate.as_view()),
    path('', views.GalleryList.as_view()),
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)