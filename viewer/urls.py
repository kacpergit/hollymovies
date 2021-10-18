from django.urls import path, include
from rest_framework.routers import DefaultRouter

from viewer.views import (
    MovieCreateView, MovieDeleteView, MovieDetailView, MovieUpdateView, MovieListView, GetMoviesApiView, GenreViewSet,
    MovieViewSet,
)

router = DefaultRouter()
router.register('genre', GenreViewSet)
router.register('movie', MovieViewSet)


app_name = 'viewer'
urlpatterns = [
    path('movie/list', MovieListView.as_view(), name='movie_list'),
    path('movie/detail/<pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>', MovieDeleteView.as_view(), name='movie_delete'),
    path('movie/api/list', GetMoviesApiView.as_view(), name='api_movie_list'),
    path('api/', include(router.urls)),
]
