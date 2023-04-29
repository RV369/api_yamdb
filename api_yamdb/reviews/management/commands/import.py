import csv

from api_yamdb.settings import PATH
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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(COMMAND_TO_IMPORT)

    def handle(self, *args, **kwargs):
        csv_model = {
            'category.csv': Categories,
            'genre.csv': Genres,
            'titles.csv': Title,
            'genre_title.csv': TitleGenre,
            'users.csv': User,
            'review.csv': Review,
            'comments.csv': Comment,
        }
        for key in csv_model.keys():
            with open(
                (f'{PATH}\\{key}'),
                encoding='utf-8',
            ) as csvfile:
                contents = csv.DictReader(csvfile)
                for row in contents:
                    record = []
                    if key == 'users.csv':
                        record = csv_model[key](
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                        )
                        record.save()
                    elif key == 'category.csv':
                        record = csv_model[key](
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                        record.save()
                    elif key == 'genre.csv':
                        record = csv_model[key](
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                        record.slug = ''.join(record.slug)
                        record.save()
                    elif key == 'genre_title.csv':
                        record = csv_model[key](
                            title_id_id=row['title_id'],
                            genre_id_id=row['genre_id'],
                        )
                        record.save()
                    elif key == 'titles.csv':
                        record = csv_model[key](
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category_id=row['category'],
                        )
                        record.save()
                    elif key == 'review.csv':
                        record = csv_model[key](
                            id=row['id'],
                            title_id=row['title_id'],
                            text=row['text'],
                            author_id=row['author'],
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                        record.save()
                    elif key == 'comments.csv':
                        record = csv_model[key](
                            id=row['id'],
                            review_id=row['review_id'],
                            text=row['text'],
                            author_id=row['author'],
                            pub_date=row['pub_date'],
                        )
                        record.save()
            self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))
