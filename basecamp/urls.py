from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "basecamp"

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),    
    path('introduction/', views.introduction, name='introduction'),
    path('bulletin_list/', views.bulletin_list, name='bulletin_list'),  
    path('meetings/', views.meetings, name='meetings'),   
    path('workers/', views.workers, name='workers'), 
    path('column/', views.column, name='column'),
    path('location/', views.location, name='location'),
    path('notice/', views.notice, name='notice'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('maps/', views.maps, name='maps'),
    path('protected/contact_list', views.serve_pdf, name='contact_list'), 
] 

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)

