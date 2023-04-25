import csv

from django.core.management.base import BaseCommand
from reviews.models import Categories, Comment, Genres, Review, Title, User

command = 'start'


FILES_DATA = (
    'category.csv',
    'genre.csv',
    'titles.csv',
    'users.csv',
    'review.csv',
    'comments.csv',
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(command)

    def handle(self, *args, **kwargs):
        for name_file_csv in FILES_DATA:
            with open(
                'J:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\'
                + name_file_csv,
                encoding='utf-8',
            ) as csvfile:
                contents = csv.DictReader(csvfile)

                for row in contents:
                    if name_file_csv == 'category.csv':
                        new_category = Categories(
                            id=row['id'], name=row['name'], slug=row['slug'],
                        )
                        new_category.save()
                    elif name_file_csv == 'genre.csv':
                        new_genre = Genres(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                        new_genre.slug = ''.join(new_genre.slug)
                        new_genre.save()
                    elif name_file_csv == 'review.csv':
                        new_review = Review(
                            title_id=row['title_id'],
                            text=row['text'],
                            author=row['author'],
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                        new_review.save()
                    elif name_file_csv == 'comments.csv':
                        new_comment = Comment(
                            review_id=row['review_id'],
                            text=row['text'],
                            author=row['author'],
                            pub_date=row['pub_date'],
                        )
                        new_comment.save()
                    elif name_file_csv == 'titles.csv':
                        new_title = Title(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category_id=row['category'],
                        )
                        new_title.save()
                    elif name_file_csv == 'users.csv':
                        new_user = User(
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                        )
                        new_user.save()
            print('Данные загружены успешно!')