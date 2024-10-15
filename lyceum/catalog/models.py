import catalog.validators
import core.models

import django.core.exceptions
import django.core.validators
import django.db


alphanumeric = django.core.validators.RegexValidator(r'^[a-zA-Z0-9_-]*$')


class Tag(core.models.AbstractModel):
    slug = django.db.models.CharField(
        unique=True,
        max_length=200,
        validators=[alphanumeric],
        verbose_name='слаг',
        help_text='напишите слаг',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name[:15]


class Category(core.models.AbstractModel):
    slug = django.db.models.CharField(
        unique=True,
        max_length=200,
        validators=[alphanumeric],
        verbose_name='слаг',
        help_text='напишите слаг',
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name='вес',
        help_text='выбирите вес',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name[:15]


class Item(core.models.AbstractModel):
    category = django.db.models.OneToOneField(
        Category, on_delete=django.db.models.CASCADE, verbose_name='категория'
    )
    text = django.db.models.TextField(
        validators=[
            catalog.validators.CustomValidator('превосходно', 'роскошно')
        ],
        verbose_name='текст',
        help_text='напишите необходимый текст',
    )
    tags = django.db.models.ManyToManyField(Tag, verbose_name='теги')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name[:15]
