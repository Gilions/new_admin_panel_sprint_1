import os
import sqlite3
from collections import defaultdict

import psycopg2
from dateutil import parser
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()

DB_PATH = '../db.sqlite'
DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT')
}

SQL = """SELECT * FROM {table};"""

postgres_data = defaultdict(list)
sqlite_data = defaultdict(list)


def load_data(sqlite_con, postgres_con):
    def postgres(postgres_con):
        # Подгружаем данные с Postgres
        cursor = postgres_con.cursor()
        query = SQL
        # Грузим с таблицы film_work
        cursor.execute(query.format(table='film_work'))
        for row in cursor.fetchall():
            postgres_data['film_work'].append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'creation_date': row['creation_date'],
                'rating': row['rating'],
                'type': row['type'],
                'created': row['created'],
                'modified': row['modified'],
                'file_path': row['file_path']
            })
        # Грузим с таблицы person
        cursor.execute(query.format(table='person'))
        for row in cursor.fetchall():
            postgres_data['person'].append({
                'id': row['id'],
                'full_name': row['full_name'],
                'created': row['created'],
                'modified': row['modified']
            })
        # Грузим с таблицы genre
        cursor.execute(query.format(table='genre'))
        for row in cursor.fetchall():
            postgres_data['genre'].append({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'created': row['created'],
                'modified': row['modified']
            })
        # Грузим с таблицы person_film_work
        cursor.execute(query.format(table='person_film_work'))
        for row in cursor.fetchall():
            postgres_data['person_film_work'].append({
                'id': row['id'],
                'film_work_id': row['film_work_id'],
                'person_id': row['person_id'],
                'role': row['role'],
                'created': row['created']
            })
        # Грузим с таблицы genre_film_work
        cursor.execute(query.format(table='genre_film_work'))
        for row in cursor.fetchall():
            postgres_data['genre_film_work'].append({
                'id': row['id'],
                'genre_id': row['genre_id'],
                'film_work_id': row['film_work_id'],
                'created': row['created']
            })

    def sqlite(sqlite_con):
        # Подгружаем данные с SQLite
        sqlite_con.row_factory = sqlite3.Row
        cursor = sqlite_con.cursor()
        query = SQL
        # Грузим с таблицы film_work
        cursor.execute(query.format(table='film_work'))
        for row in cursor.fetchall():
            sqlite_data['film_work'].append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'creation_date': row['creation_date'],
                'rating': row['rating'],
                'type': row['type'],
                'created': parser.parse(row['created_at']),
                'modified': parser.parse(row['updated_at']),
                'file_path': row['file_path']
            })
        # Грузим с таблицы genre
        cursor.execute(query.format(table='genre'))
        for row in cursor.fetchall():
            sqlite_data['genre'].append({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'created': parser.parse(row['created_at']),
                'modified': parser.parse(row['updated_at'])
            })
        # Грузим с таблицы person
        cursor.execute(query.format(table='person'))
        for row in cursor.fetchall():
            sqlite_data['person'].append({
                'id': row['id'],
                'full_name': row['full_name'],
                'created': parser.parse(row['created_at']),
                'modified': parser.parse(row['updated_at'])
            })
        # Грузим с таблицы person_film_work
        cursor.execute(query.format(table='person_film_work'))
        for row in cursor.fetchall():
            sqlite_data['person_film_work'].append({
                'id': row['id'],
                'film_work_id': row['film_work_id'],
                'person_id': row['person_id'],
                'role': row['role'],
                'created': parser.parse(row['created_at'])
            })
        # Грузим с таблицы genre_film_work
        cursor.execute(query.format(table='genre_film_work'))
        for row in cursor.fetchall():
            sqlite_data['genre_film_work'].append({
                'id': row['id'],
                'genre_id': row['genre_id'],
                'film_work_id': row['film_work_id'],
                'created': parser.parse(row['created_at'])
            })

    sqlite(sqlite_con)
    postgres(postgres_con)


if __name__ == '__main__':
    with sqlite3.connect(DB_PATH) as sqlite_conn, psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_data(sqlite_conn, pg_conn)

    # Проверяем количество записей таблицы film_work
    first_arg = len(postgres_data['film_work'])
    second_arg = len(sqlite_data['film_work'])
    assert (first_arg == second_arg)

    # Проверяем количество записей таблицы genre
    first_arg = len(postgres_data['genre'])
    second_arg = len(sqlite_data['genre'])
    assert first_arg == second_arg

    # Проверяем количество записей таблицы person
    first_arg = len(postgres_data['person'])
    second_arg = len(sqlite_data['person'])
    assert first_arg == second_arg

    # Проверяем количество записей таблицы person_film_work
    first_arg = len(postgres_data['person_film_work'])
    second_arg = len(sqlite_data['person_film_work'])
    assert first_arg == second_arg

    # Проверяем количество записей таблицы genre_film_work
    first_arg = len(postgres_data['genre_film_work'])
    second_arg = len(sqlite_data['genre_film_work'])
    assert first_arg == second_arg

    # Проверяем состав film_work
    first_arg = postgres_data['film_work']
    second_arg = sqlite_data['film_work']
    assert first_arg == second_arg

    # Проверяем состав genre
    first_arg = postgres_data['genre']
    second_arg = sqlite_data['genre']
    assert first_arg == second_arg

    # Проверяем состав person
    first_arg = postgres_data['person']
    second_arg = sqlite_data['person']
    assert first_arg == second_arg

    # Проверяем состав person_film_work
    first_arg = postgres_data['person_film_work']
    second_arg = sqlite_data['person_film_work']
    assert first_arg == second_arg

    # Проверяем состав genre_film_work
    first_arg = postgres_data['genre_film_work']
    second_arg = sqlite_data['genre_film_work']
    assert first_arg == second_arg
