import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FilmType:
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'

    CHOICES = [
        (MOVIE, 'Фильм'),
        (TV_SHOW, 'Сериал'),
    ]


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full_name', max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Person'
        verbose_name_plural = 'Person'

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField('rating', blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField('type', choices=FilmType.CHOICES, default=FilmType.MOVIE,
                            max_length=60)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Filmwork'
        verbose_name_plural = 'Filmwork'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
