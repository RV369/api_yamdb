from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_username, validate_year

LEN_TEXT = 15


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    ]
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        default='XXXX',
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance,
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Categories(models.Model):
    name = models.CharField(
        unique=True,
        verbose_name='имя категории',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genres(models.Model):
    name = models.CharField(
        unique=True,
        verbose_name='Жанр',
        max_length=256,
    )

    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        max_length=50,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        db_index=True,
    )
    year = models.PositiveIntegerField(
        'год',
        validators=(validate_year,),
        db_index=True,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='жанр',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey(
        Title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    genre_id = models.ForeignKey(
        Genres,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Произведение-Жанр'
        verbose_name_plural = 'Произведения-Жанры'

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    MIN_SCORE = 1
    MAX_SCORE = 10
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        db_constraint=False,
    )
    text = models.CharField(
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
        db_constraint=False,
    )
    score = models.PositiveSmallIntegerField(
        'оценка',
        validators=(
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'},
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique review',
            ),
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:LEN_TEXT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    text = models.CharField(
        'текст комментария',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
        db_constraint=False,
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LEN_TEXT]
