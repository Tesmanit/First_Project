from django import forms
from .models import Beat, Author
from django_select2 import forms as s2forms


class AuthorWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        'name__iregex',
    ]
class GenreWidget(s2forms.Select2Widget):
    search_fields = [
        'genre_name__iregex',
    ]

class AlbumWidget(s2forms.Select2Widget):
    search_fields = [
        'album_name__iregex',
    ]

class BeatAdditionForm(forms.ModelForm):
    class Meta:
        model = Beat
        fields = ['url', 'name', 'audio', 'genre', 'author', 'album']

        widgets = {
            'author': AuthorWidget,
            'genre': GenreWidget,
            'album': AlbumWidget
        }



class AtristAdditionForm(forms.ModelForm):
    image = forms.FileField(required=True, label="Фото артиста(обязательно)")
    class Meta:
        model = Author
        fields = ['name', 'image']