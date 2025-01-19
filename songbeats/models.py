import random

from django.db import models
from django.urls import reverse
from accounts.models import User
from pytils.translit import slugify


class Genre(models.Model):
    genre_name = models.CharField(verbose_name='Название жанра', max_length=20, blank=True, null=True)
    description = models.TextField(verbose_name='Описание жанра', blank=True)
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.genre_name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return 'Жанр ' + self.genre_name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

class Author(models.Model):
    def content_file_name(instance, filename):
        return '/'.join(['images/artists', instance.name[0], filename])

    name = models.CharField(verbose_name='Псевдоним автора', max_length=50)
    slug = models.SlugField(default='', null=False, db_index=True)
    image = models.ImageField(default='images/default-artist.jpg', upload_to=content_file_name)
    is_published = models.BooleanField(verbose_name="Выкладывать?", default=False)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Кто добавил?")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist', kwargs={'artist_slug': self.slug})

class Album(models.Model):

    def content_file_name(instance, filename):
        return '/'.join(['images', instance.album_name[0], filename])

    album_name = models.CharField('Название альбома', max_length=50)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, verbose_name='Автор альбома', blank=True, null=True, related_name='album')
    cover = models.ImageField(verbose_name='Обложка альбома', blank=True, upload_to=content_file_name)
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.album_name)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.album_name


class Beat(models.Model):

    def content_file_name(instance, filename):
        return '/'.join(['content', instance.name[0], filename])
    url = models.CharField(verbose_name='Ссылка на бит', max_length=200, blank=True)
    name = models.CharField(verbose_name='Название трека', max_length=50)
    audio = models.FileField(verbose_name='Файл с битом',upload_to=content_file_name)
    slug = models.SlugField(default='', null=False, db_index=True)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, verbose_name='Жанр трека', blank=True, null=True, related_name='beats')
    author = models.ManyToManyField(Author, verbose_name='Исполнитель(исполнители) трека', blank=True, related_name='beats')
    album = models.ForeignKey(Album, on_delete=models.DO_NOTHING, verbose_name='Альбом', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="Выкладывать?", default=False)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Кто добавил?")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)+str(random.randint(1,9*10^5))
        super(Beat, self).save(*args, **kwargs)

    authors = ''

    def __str__(self):
        for author in list(self.author.all()):
            self.authors += str(author) + ' '
        return self.authors + '- ' + self.name