from itertools import islice
from typing import Dict

import psycopg2

from data_classes import FilmWork
from data_classes import Genre
from data_classes import GenreFilmwork
from data_classes import Person
from data_classes import PersonFilmWork


class PostgresSaver:
    """Класс загружает данные в базу данных Postgres
    Args:
        connection(psycopg2.extensions.connection): connection
        chunk(int): Делитель
    """
    def __init__(self, connection: psycopg2.extensions.connection, chunk: int = 100):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.chunk = chunk

    def _film_work(self, film_works: [FilmWork]):
        SQL = """
        INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created,  modified, file_path)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """

        for chunk in self._chunks(film_works, self.chunk):
            for row in chunk:
                self.cursor.execute(SQL, (
                    row.id,
                    row.title,
                    row.description,
                    row.creation_date,
                    row.rating,
                    row.type,
                    row.created,
                    row.modified,
                    row.file_path
                ))
            self.connection.commit()

    def _person(self, persons: [Person]):
        SQL = """
        INSERT INTO content.person (id, full_name, created,  modified)
        VALUES(%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """
        for chunk in self._chunks(persons, self.chunk):
            for row in chunk:
                self.cursor.execute(SQL, (
                    row.id,
                    row.full_name,
                    row.created,
                    row.modified
                ))
            self.connection.commit()

    def _genre(self, genres: [Genre]):
        SQL = """
        INSERT INTO content.genre (id, name, description, created,  modified)
        VALUES(%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """
        for chunk in self._chunks(genres, self.chunk):
            for row in chunk:
                self.cursor.execute(SQL, (
                    row.id,
                    row.name,
                    row.description,
                    row.created,
                    row.modified
                ))
            self.connection.commit()

    def _person_film_work(self, person_film_works: [PersonFilmWork]):
        SQL = """
        INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created)
        VALUES(%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """
        for chunk in self._chunks(person_film_works, self.chunk):
            for row in chunk:
                self.cursor.execute(SQL, (
                    row.id,
                    row.film_work,
                    row.person,
                    row.role,
                    row.created
                ))
            self.connection.commit()

    def _genre_film_work(self, genre_film_works: [GenreFilmwork]):
        SQL = """
        INSERT INTO content.genre_film_work (id, genre_id, film_work_id, created)
        VALUES(%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """
        for chunk in self._chunks(genre_film_works, self.chunk):
            for row in chunk:
                self.cursor.execute(SQL, (
                    row.id,
                    row.genre,
                    row.film_work,
                    row.created
                ))
            self.connection.commit()

    @staticmethod
    def _chunks(iterable, n):
        it = iter(iterable)
        chunk = list(islice(it, n))
        while chunk:
            yield chunk
            chunk = list(islice(it, n))

    def _router(self, data: Dict[str, list]):
        for table, value in data.items():
            if table == 'film_work':
                self._film_work(value)
            elif table == 'person':
                self._person(value)
            elif table == 'genre':
                self._genre(value)
            elif table == 'person_film_work':
                self._person_film_work(value)
            elif table == 'genre_film_work':
                self._genre_film_work(value)

    def run(self, data: Dict[str, list]):
        self._router(data)
