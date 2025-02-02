from django.urls import path
from gallery import views

urlpatterns = [
    # path('users/', views.UserList.as_view(), name='user-list'),
    # path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('albums/', views.AlbumListCreate.as_view(), name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetail.as_view(), name='album-detail'),
    path('photos/', views.PhotoList.as_view(), name='photo-list'),
    path('photos/<int:pk>/', views.PhotoDetail.as_view(), name='photo-detail'),
    path('videos/', views.VideoListCreate.as_view(), name='video-list'),
    path('videos/<int:pk>/', views.VideoDetail.as_view(), name='video-detail'),
]