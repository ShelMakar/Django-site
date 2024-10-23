import re

import django.core.exceptions
import django.core.validators
import django.db
import django.templatetags.static
import django.utils.safestring
import django_cleanup.cleanup
import sorl.thumbnail

import catalog.validators
import core.models

alphanumeric = django.core.validators.RegexValidator(r'^[a-zA-Z0-9_-]*$')


def corr_name(value):
    value = re.sub(r'[^\w]', '', value).lower()
    target = 'abekmhopctyx'
    replacer = 'авекмнорстух'
    for i in range(len(value)):
        if value[i] in target:
            j = target.find(value[i])
            value = value.replace(target[j], replacer[j])
    return value


class Tag(core.models.NormName):
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


class Category(core.models.NormName):
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
    category = django.db.models.ForeignKey(
        'category',
        on_delete=django.db.models.CASCADE,
        related_name='category_items',
    )
    text = django.db.models.TextField(
        validators=[
            catalog.validators.CustomValidator('превосходно', 'роскошно'),
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


@django_cleanup.cleanup.select
class MainImage(django.db.models.Model):
    main_images = django.db.models.ImageField(
        ('Будет приведено к размеру 300х300'),
        upload_to='uploads/',
        help_text='Выберите изображение',
    )
    main_image = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name='главное изображение',
        null=True,
        blank=True,
        related_name='mainimage',
    )

    def image_tmb(self):
        if self.main_images:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.main_images.url}" width="50">',
            )
        return 'image not found'

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_images,
            '300',
            crop='center',
            quality=51,
        )

    class Meta:
        verbose_name = 'превью'
        verbose_name_plural = 'изображения'

    image_tmb.short_description = 'первью'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.main_images.name


@django_cleanup.cleanup.select
class SecondImages(django.db.models.Model):
    image = django.db.models.ImageField(
        ('Будет приведено к размеру 300х300'),
        upload_to='uploads/',
        help_text='Выберите изображение',
    )
    images = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name='изображения',
        null=True,
        blank=True,
    )

    def image_tmb(self):
        if self.images:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.images.url}" width="50">',
            )
        return 'image not found'

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.images,
            '300',
            crop='center',
            quality=51,
        )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    image_tmb.short_description = 'первью'
    image_tmb.allow_tags = True

    def __str__(self):
        return self.images.name


__all__ = ['SecondImages', 'Item', 'MainImage', 'Category', 'Tag', 'corr_name']
