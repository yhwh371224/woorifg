from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    BulletinListView, 
    BulletinDetailView, 
    MemberListView, 
    MemberDetailView, 
    PdfListView, 
    PdfDetailView, 
    MusicListView, 
    MusicDetailView
)
from . import views


urlpatterns = [
    path('search/<str:q>/', views.MusicSearch.as_view(), name='music_search'),
    path('category/<str:slug>/', views.MusicListByCategory.as_view(), name='music_list_by_category'),
    path('bulletins/', BulletinListView.as_view(), name='bulletin_list'),
    path('bulletins/<int:pk>/', BulletinDetailView.as_view(), name='bulletin_detail'),
    path('pdfs/', PdfListView.as_view(), name='pdf_list'),
    path('pdfs/<int:pk>/', PdfDetailView.as_view(), name='pdf_detail'),
    path('musics/', MusicListView.as_view(), name='music_list'),
    path('musics/<int:pk>/', MusicDetailView.as_view(), name='music_detail'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member_detail'),
    path('upload/', views.BulletinUploadView.as_view(), name='bulletin_upload'),
    path('pdf_upload/', views.PdfUploadView.as_view(), name='pdf_upload'),
    path('music_upload/', views.MusicUploadView.as_view(), name='music_upload'),
    path('merge-pdfs/', views.merge_latest_pdfs, name='merge_pdfs'),
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)