from django.urls import path
from gallery import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('albums/', views.AlbumListCreate.as_view(), name='album-list'),
    path('album/<int:album_id>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('media/', views.MediaList.as_view(), name='media-list'),
    path('media/<int:media_id>/', views.MediaDetail.as_view(), name='media-detail'),
    path('media/create/', views.MediaCreate.as_view(), name='media-create'),
]