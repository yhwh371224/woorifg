from django.urls import path
from .views import BulletinListView, BulletinDetailView, MemberListView, MemberDetailView, PdfListView, PdfDetailView
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('bulletins/', BulletinListView.as_view(), name='bulletin_list'),
    path('bulletins/<int:pk>/', BulletinDetailView.as_view(), name='bulletin_detail'),
    path('pdfs/', PdfListView.as_view(), name='pdf_list'),
    path('pdfs/<int:pk>/', PdfDetailView.as_view(), name='pdf_detail'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member_detail'),
    path('upload/', views.BulletinUploadView.as_view(), name='bulletin_upload'),
    path('pdf_upload/', views.PdfUploadView.as_view(), name='pdf_upload'),
    path('merge-pdfs/', views.merge_latest_pdfs, name='merge_pdfs'),
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)