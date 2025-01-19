from django.contrib import admin
from django.urls import reverse

from .models import Author, Beat, Genre, Album
from accounts.models import User
admin.site.site_header = 'Трек админ'
admin.site.index_title = 'Администрирование треков'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published", "added_by"]
    search_fields = ["added_by__username"]
    list_editable = ["is_published"]
    exclude = ['slug']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    exclude = ['slug']


@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published", "added_by"]
    search_fields = ["added_by__username"]
    list_editable = ["is_published"]
    exclude = ['slug']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    exclude = ['slug']
