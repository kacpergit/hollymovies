from viewer.views import MovieListView


class IndexView(MovieListView):
    template_name = 'movies.html'
    extra_context = {
        "x": 3,
        "y": "MobByN"
    }
