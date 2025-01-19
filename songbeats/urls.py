from django.urls import path
from .views import test, artists, artist, genres, genre, addition, artistaddition


urlpatterns = [
    path('', test, name = 'home'),
    path('artists/', artists, name = 'artists'),
    path('artist/<slug:artist_slug>/', artist, name = 'artist'),
    path('genres/', genres, name = 'genres'),
    path('genre/<slug:genre_slug>/', genre, name = 'genre'),
    path('add_beat', addition, name = 'add_beat'),
    path('add_artist', artistaddition, name = 'add_artist'),
]
