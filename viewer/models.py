from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
    DateTimeField, ImageField


class Genre(Model):
    name = CharField(max_length=120)

    def __str__(self):
        return self.name


class Movie(Model):
    title = CharField(max_length=128)
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    rating = IntegerField()
    released = DateField()
    description = TextField(null=True, blank=True)
    poster = ImageField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.released.year})"
