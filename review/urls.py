from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'review'

urlpatterns = [
    path('search/<str:q>/', views.PostSearch.as_view(), name='review_search'),
    path('category/<str:slug>/', views.PostListByCategory.as_view(), name='review_list_by_category'),
    path('', views.PostList.as_view(), name="review"),
    path('create/', views.PostCreate.as_view(), name="review_create"),
    path('<int:pk>/', views.PostDetail.as_view(), name="review_detail"),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name="review_update"),
    path('<int:pk>/new_comment/', views.CommentCreate.as_view(), name='new_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]
