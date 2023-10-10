from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from django.db import models
from django.db.models import UniqueConstraint

from core.constants import FIELD_LENGTH
from core.validators import current_year
from users.models import User


class NameSlug(models.Model):
    """Базовый класс для жанра и категории"""
    name = models.CharField(
        verbose_name='Наименование',
        max_length=FIELD_LENGTH['MAX_SIZE']
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:50]


class Category(NameSlug):
    """Категории."""
    class Meta(NameSlug.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlug):
    """Жанр."""
    class Meta(NameSlug.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        verbose_name='Наименование',
        max_length=FIELD_LENGTH['MAX_SIZE']
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[
            MaxValueValidator(current_year),
        ],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:50]


class TitleGenre(models.Model):
    """Жанр произведения."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение.',
        on_delete=models.CASCADE,
        related_name='genres'
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        related_name='titles'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title', 'genre'], name='unique genre')
        ]
        verbose_name = 'Произведение, Жанр'


class TextAuthor(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]


class Review(TextAuthor):
    """Отзыв произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка отзыва",
        validators=[
            MinValueValidator(1, 'Введите значение от 1 до 10'),
            MaxValueValidator(10, 'Введите значение от 1 до 10')
        ],
    )

    class Meta(TextAuthor.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]


class Comment(TextAuthor):
    """Комментарий к отзыву произведения."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )

    class Meta(TextAuthor.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
