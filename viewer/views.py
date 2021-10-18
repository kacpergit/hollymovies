from logging import getLogger

from django.urls import reverse_lazy

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from hollymovies.mixins import TitleMixin
from viewer.models import Movie, Genre
from django.views.generic import UpdateView, DeleteView, ListView, DetailView, CreateView
from viewer.forms import MovieForm
from viewer.serializers import GenreSerializer, MovieSerializer

LOGGER = getLogger()


class GenreViewSet(ModelViewSet):

    queryset = Genre.objects
    serializer_class = GenreSerializer
    renderer_classes = APIView.renderer_classes + [XMLRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class MovieViewSet(ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


def movies(request):
    return render(
        request,
        template_name='movies.html',
        context={'movies': Movie.objects.all()}
    )



class MovieListView(TitleMixin, ListView):
    template_name = 'movie_list.html'
    model = Movie
    paginate_by = 30



class MovieDetailView(DetailView):
    template_name = 'movie_detail.html'
    model = Movie

    def get_title(self):
        return self.object.title


class MovieCreateView(LoginRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = MovieForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)

    success_url = reverse_lazy('viewer:movie_list')


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        LOGGER.warning('User provided incorrect data while updating movie.')
        return super().form_invalid(form)

    success_url = reverse_lazy('viewer:movie_list')

    def get_queryset(self):
        return Movie.objects.filter(id__lte=10)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('viewer:movie_list')


class MoviesView(LoginRequiredMixin, ListView):
    template_name = 'movies.html'
    model = Movie


class GetMoviesApiView(View):

    def get(self, *_, **__):
        movies = [
            {
                'title': movie.title,
                'genre': movie.genre.name,
                'rating': movie.rating
            }
            for movie in Movie.objects.all()
        ]
        return JsonResponse({'movies': movies})
