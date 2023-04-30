import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import (
    Categories,
    Comment,
    Genres,
    Review,
    Title,
    TitleGenre,
    User,
)

COMMAND_TO_IMPORT = 'start'

PATH = Path.cwd() / 'static' / 'data'


def add_category(row):
    category = Categories(id=row['id'], name=row['name'], slug=row['slug'])
    category.save()


def add_genre(row):
    genre = Genres(id=row['id'], name=row['name'], slug=row['slug'])
    genre.slug = ''.join(genre.slug)
    genre.save()


def add_title(row):
    title = Title(
        id=row['id'],
        name=row['name'],
        year=row['year'],
        category_id=row['category'],
    )
    title.save()


def add_genre_title(row):
    genre_title = TitleGenre(
        title_id_id=row['title_id'],
        genre_id_id=row['genre_id'],
    )
    genre_title.save()


def add_users(row):
    user = User(
        username=row['username'],
        email=row['email'],
        role=row['role'],
        bio=row['bio'],
        first_name=row['first_name'],
        last_name=row['last_name'],
    )
    user.save()


def add_review(row):
    review = Review(
        id=row['id'],
        title_id=row['title_id'],
        text=row['text'],
        author_id=row['author'],
        score=row['score'],
        pub_date=row['pub_date'],
    )
    review.save()


def add_comment(row):
    comment = Comment(
        id=row['id'],
        review_id=row['review_id'],
        text=row['text'],
        author_id=row['author'],
        pub_date=row['pub_date'],
    )
    comment.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(COMMAND_TO_IMPORT)

    def handle(self, *args, **kwargs):
        imported_models = {
            'category.csv': add_category,
            'genre.csv': add_genre,
            'titles.csv': add_title,
            'genre_title.csv': add_genre_title,
            'users.csv': add_users,
            'review.csv': add_review,
            'comments.csv': add_comment,
        }

        for key in imported_models.keys():
            with open((f'{PATH}\\{key}'), encoding='utf-8') as csvfile:
                contents = csv.DictReader(csvfile)
                for row in contents:
                    imported_models[key](row)
        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))
