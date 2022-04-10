import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: datetime
    rating: float
    created: datetime
    modified: datetime
    file_path: str
    certificate: str = field(default=None)
    type: str = field(default='movie')
    id: uuid.UUID = field(default_factory=uuid.UUID)


@dataclass
class Genre:
    name: str
    description: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.UUID)


@dataclass
class PersonFilmWork:
    role: str
    created: datetime
    film_work: uuid.UUID = field(default_factory=uuid.UUID)
    person: uuid.UUID = field(default_factory=uuid.UUID)
    id: uuid.UUID = field(default_factory=uuid.UUID)


@dataclass
class Person:
    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.UUID)


@dataclass
class GenreFilmwork:
    created: datetime
    film_work: uuid.UUID = field(default_factory=uuid.UUID)
    genre: uuid.UUID = field(default_factory=uuid.UUID)
    id: uuid.UUID = field(default_factory=uuid.UUID)
