import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from postgresql import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite import SQLiteLoader

load_dotenv()

TABLES = ['film_work', 'genre', 'person', 'person_film_work', 'genre_film_work']
DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT')
}


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    sqlite_data = sqlite_loader.run(TABLES)
    postgres_saver.run(sqlite_data)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
