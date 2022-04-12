import sqlite3
from collections import defaultdict

from data_classes import FilmWork, Genre, GenreFilmwork, Person, PersonFilmWork


class SQLiteLoader:
    """Класс Подгружает данные из базы данных SQLite
    Args:
        connection(sqlite3.connect): connection
    Return:
        Dict[str:list]
    """
    SQL = """
    SELECT * FROM {table};
    """

    def __init__(self, connection: sqlite3.connect):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.curs = self.connection.cursor()
        self.all_data = defaultdict(list)

    def _film_work(self, data: list):
        for row in data:
            self.all_data['film_work'].append(
                FilmWork(
                    title=row['title'],
                    description=row['description'],
                    creation_date=row['creation_date'],
                    rating=row['rating'],
                    created=row['created_at'],
                    modified=row['updated_at'],
                    file_path=row['file_path'],
                    type=row['type'],
                    id=row['id']
                )
            )

    def _person(self, data: list):
        for row in data:
            self.all_data['person'].append(
                Person(
                    id=row['id'],
                    full_name=row['full_name'],
                    created=row['created_at'],
                    modified=row['updated_at']
                )
            )

    def _genre(self, data: list):
        for row in data:
            self.all_data['genre'].append(
                Genre(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created=row['created_at'],
                    modified=row['updated_at']
                )
            )

    def _person_film_work(self, data: list):
        for row in data:
            self.all_data['person_film_work'].append(
                PersonFilmWork(
                    id=row['id'],
                    film_work=row['film_work_id'],
                    person=row['person_id'],
                    role=row['role'],
                    created=row['created_at']
                )
            )

    def _genre_film_work(self, data: list):
        for row in data:
            self.all_data['genre_film_work'].append(
                GenreFilmwork(
                    id=row['id'],
                    genre=row['genre_id'],
                    film_work=row['film_work_id'],
                    created=row['created_at']
                )
            )

    def _make_request(self, tables: [str], size=500):
        for table in tables:
            self.curs.execute(self.SQL.format(table=table))
            data = []
            rows = self.curs.fetchmany(size)
            while rows:
                for row in rows:
                    data.append(row)
                rows = self.curs.fetchmany(size)

            if table == 'film_work':
                self._film_work(data)
            elif table == 'genre':
                self._genre(data)
            elif table == 'person':
                self._person(data)
            elif table == 'person_film_work':
                self._person_film_work(data)
            elif table == 'genre_film_work':
                self._genre_film_work(data)

    def run(self, tables: [str]):
        self._make_request(tables)
        self.curs.close()
        return self.all_data
