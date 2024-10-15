import django.core.exceptions
import django.core.validators
import django.db

import catalog.validators

import core.models


alphanumeric = django.core.validators.RegexValidator(r'^[a-zA-Z0-9_-]*$')

import django.core.exceptions


def custom_validator(value):
    if 'превосходно' not in value and 'роскошно' not in value:
        raise django.core.exceptions.ValidationError(
            'в слове нет необходимых слов'
        )


class Tag(core.models.AbstractModel):
    slug = django.db.models.CharField(
        unique=True,
        max_length=200,
        validators=[alphanumeric],
        verbose_name='Слаг',
        help_text='напишите слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:15]


class Category(core.models.AbstractModel):
    slug = django.db.models.CharField(
        unique=True,
        max_length=200,
        validators=[alphanumeric],
        verbose_name='Слаг',
        help_text='напишите слаг',
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name='Вес',
        help_text='выбирите вес',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Item(core.models.AbstractModel):
    category = django.db.models.OneToOneField(
        Category, on_delete=django.db.models.CASCADE, verbose_name='Категория'
    )
    text = django.db.models.TextField(
        validators=[
            catalog.validators.CustomValidator('превосходно', 'роскошно')
        ],
        verbose_name='Текст',
        help_text='напишите необходимый текст',
    )
    tags = django.db.models.ManyToManyField(Tag, verbose_name='Теги')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name[:15]
