from django.urls import path
from gallery import views
from gallery import admin_views

urlpatterns = [
    path('users/', admin_views.UserList.as_view(), name='user-list'),
    path('user/<int:pk>/', admin_views.UserDetail.as_view(), name='user-details'),
    path('albums/', views.AlbumListCreate.as_view(), name='album-list'),
    path('albums/<int:album_id>/', views.AlbumDetailView.as_view(), name='album-details'),
    path('albums/<str:album_identifier>/media/', views.AlbumMediaList.as_view(), name='album-media-list'),
    path('media/<int:media_id>/', views.MediaDetail.as_view(), name='media-details'),
    path('media/create/', views.MediaCreate.as_view(), name='media-create'),
]

# TODO: Views should handle thumbnails, media uploads, and media downloads
# TODO: Start working on the frontend to display the gallery and work with the API
# to do the above TODO: subdivide the frontend into components and start with the simplest one
# TODO: handle jwt authentication in the frontend
# TODO: only https should be allowed
# NOTE: NOT STORING JWT IN LOCAL STORAGE, USE HTTP ONLY COOKIES INSTEAD, and check for CSRF

##########################################################################################################
""" TODO: GO THROUGH THE PROJECT AND WRITE OUT WHAT WAS THE PLAN AGAIN, GET NEW PLAN WITH SUBDIVIDED TASKS
SO IT'S EASIER TO WORK KEEP WORKING AND REMEMBER WHAT TO DO NEXT"""
##########################################################################################################