from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, Count, F
from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse_lazy
# from django.views.generic import FormView
from django.views.decorators.cache import cache_page
from .models import Beat, Author, Genre
from .forms import BeatAdditionForm, AtristAdditionForm


@cache_page(60)
def test(request):
    if (request.GET.get('beat_search')):
        beats = (Beat.objects.filter(
             Q(is_published=True)
             &(Q(name__iregex=request.GET.get('beat_search'))
             |Q(author__name__iregex=request.GET.get('beat_search'))))
             .select_related('album')
             .prefetch_related('author')
             )
    else:
        beats = (Beat.objects
             .filter(Q(is_published=True))
             .select_related('album')
             .prefetch_related('author')
             )
    p = Paginator(beats, 12)
    page_number = request.GET.get('page')
    page_objects = p.get_page(page_number)
    if (request.GET.get('beat_search')):
        title = f'Результаты поиска по запросу {(request.GET.get("beat_search"))}' + ', страница: ' \
                + (str(page_number) if page_number else '1')
    else:
        title = 'Все биты' + ', страница: ' + (str(page_number) if page_number else '1')
    context = {
        'page_objects': page_objects,
        'title': title,
        'search': 'Поиск трека или автора',
    }
    return render(request, 'songbeats/frst.html', context)


def artists(request):
    if (request.GET.get('beat_search')):
        artists = Author.objects.annotate(count=Count(F('beats'))).filter(Q(name__iregex=request.GET.get('beat_search'))
                                                                          &Q(is_published=True)&Q(count__gt=0))
    else:
        artists = Author.objects.annotate(count=Count(F('beats'))).filter(Q(is_published=True)&Q(count__gt=0))
    p = Paginator(artists, 12)
    page_number = request.GET.get('page')
    page_objects = p.get_page(page_number)
    if (request.GET.get('beat_search')):
        title = f'Исполнитель по запросу {(request.GET.get("beat_search"))}' + ', страница: ' \
                + (str(page_number) if page_number else '1')
    else:
        title = 'Все исполнители' + ', страница: ' + (str(page_number) if page_number else '1')
    context = {
        'page_objects': page_objects,
        'search': 'Поиск исполнителя',
        'title': title
    }
    return render(request, 'songbeats/artists.html', context)

def artist(request, artist_slug):
    if (request.GET.get('beat_search')):
        artist = get_object_or_404(Author.objects.prefetch_related(Prefetch('beats',
    queryset=Beat.objects.filter(Q(name__iregex=(request.GET.get('beat_search')))
                                 &Q(is_published=True)).select_related('album'))), slug=artist_slug)
    else:
        artist = get_object_or_404(Author.objects.prefetch_related(Prefetch('beats',
    queryset=Beat.objects.filter(is_published=True).select_related('album'))), slug=artist_slug)
    p = Paginator(artist.beats.all(), 12)
    page_number = request.GET.get('page')
    page_objects = p.get_page(page_number)
    if (request.GET.get('beat_search')):
        title = 'Треки исполнителя ' + artist.name + f' по запросу {(request.GET.get("beat_search"))}' \
                +', страница: ' + (str(page_number) if page_number else '1')
    else:
        title = 'Треки исполнителя ' + artist.name + ', страница: ' + (str(page_number) if page_number else '1')
    context = {
        'title': title,
        'artist': artist,
        'page_objects': page_objects,
        'search': 'Поиск трека'
    }
    return render(request, 'songbeats/artist.html', context)

def genres(request):
    if (request.GET.get('beat_search')):
        genres = Genre.objects.annotate(count=Count(F('beats')))\
            .filter(Q(genre_name__iregex=(request.GET.get('beat_search')))&Q(count__gt=0))
    else:
        genres = Genre.objects.annotate(count=Count(F('beats'))).filter(count__gt=0)
    p = Paginator(genres, 24)
    page_number = request.GET.get('page')
    page_objects = p.get_page(page_number)
    if (request.GET.get('beat_search')):
        title = f'Жанры по запросу {(request.GET.get("beat_search"))}' + ', страница: ' \
                + (str(page_number) if page_number else '1')
    else:
        title = 'Все жанры' + ', страница: ' + (str(page_number) if page_number else '1')
    context = {
        'page_objects': page_objects,
        'title': title,
        'search': 'Поиск жанра'
    }
    return render(request, 'songbeats/genres.html', context)


def genre(request, genre_slug):
    if (request.GET.get('beat_search')):
        genre = get_object_or_404(Genre.objects.prefetch_related(Prefetch('beats',
    queryset=Beat.objects.filter(Q(is_published=True)&Q(name__iregex=(request.GET.get('beat_search'))))
        .select_related('album')
        .prefetch_related('author'))),slug=genre_slug)
    else:
        genre = get_object_or_404(Genre.objects.prefetch_related(Prefetch('beats',
    queryset=Beat.objects.filter(is_published=True)
        .select_related('album').prefetch_related('author'))), slug=genre_slug)
    p = Paginator(genre.beats.all(), 12)
    page_number = request.GET.get('page')
    page_objects = p.get_page(page_number)
    if (request.GET.get('beat_search')):
        title = 'Биты жанра ' + genre.genre_name + f' по запросу {(request.GET.get("beat_search"))}' \
                + ', страница: ' + (str(page_number) if page_number else '1')
    else:
        title = 'Биты жанра ' + genre.genre_name + ', страница: ' + (str(page_number) if page_number else '1')
    context = {
        'title': title,
        'page_objects': page_objects,
        'search': 'Поиск трека'
    }
    return render(request, 'songbeats/genre.html', context)


def addition(request):
    if request.method == 'POST':
        form = BeatAdditionForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.added_by = request.user
            order.save()
            form.save_m2m()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = BeatAdditionForm()

    context = {
        'title': 'Добавление бита',
        'form': form,
        'button_content': 'Добавить бит'
    }
    return render(request, 'songbeats/addition.html', context)


# class Addition(FormView):
#     form_class = BeatAdditionForm
#     template_name = 'songbeats/addition.html'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, **kwargs):
#         ctx=super().get_context_data(**kwargs)
#         ctx['title'] = 'Добавление бита'
#         ctx['button_content'] = 'Добавить бит'
#         return ctx
#     def form_valid(self, form):
#         order = form.save(commit=False)
#         order.added_by = self.request.user
#         order.save()
#         form.save_m2m()
#         return super(Addition, self).form_valid(form)
#

def artistaddition(request):
    if request.method == 'POST':
        form = AtristAdditionForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.added_by = request.user
            order.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = AtristAdditionForm()
    context = {
        'title': 'Добавление исполнителя',
        'form': form,
        'button_content': 'Добавить исполнителя'
    }
    return render(request, 'songbeats/addition.html', context)

