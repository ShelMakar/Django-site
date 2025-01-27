__all__ = [
    "Item",
    "Gallery",
    "Tag",
    "Category",
]

import re

import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.safestring
import sorl.thumbnail
import tinymce.models
import transliterate

import catalog.validators
import core.models


def normalize_string(normalize_string):
    normalize_string = re.sub(
        r"[0-9!#$%&'()*+,\-./:;<=>?@_~^№]",
        "",
        "".join(normalize_string.lower().strip().split()),
    )

    return transliterate.translit(normalize_string, "ru")


class ItemManager(django.db.models.Manager):
    def on_main(self):
        queryset = self.get_queryset()

        filtered_queryset = queryset.filter(
            is_on_main=True,
            is_published=True,
            category__is_published=True,
        )

        ordered_queryset = filtered_queryset.order_by("category__name")

        related_queryset = ordered_queryset.select_related("category")

        prefetch_queryset = related_queryset.prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )

        return prefetch_queryset.only(
            "id",
            "name",
            "text",
            "category__name",
        )

    def published(self):
        queryset = self.get_queryset()

        filtered_queryset = queryset.filter(
            is_published=True,
            category__is_published=True,
        )

        ordered_queryset = filtered_queryset.order_by("category__name")

        related_queryset = ordered_queryset.select_related("category")

        prefetch_queryset = related_queryset.prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )

        return prefetch_queryset.only(
            "id",
            "name",
            "text",
            "category__name",
        )


class Item(core.models.AbstactModel):
    objects = ItemManager()

    text = tinymce.models.HTMLField(
        verbose_name="текст",
        validators=[
            catalog.validators.CustomValidator("превосходно", "роскошно"),
        ],
        help_text="Введите текст",
    )

    category = django.db.models.ForeignKey(
        "Category",
        on_delete=django.db.models.CASCADE,
        help_text="Выберите категорию",
        verbose_name="категория",
    )

    tags = django.db.models.ManyToManyField(
        "Tag",
        help_text="Выберите тег/теги",
        verbose_name="теги",
    )

    MainImage = django.db.models.ImageField(
        upload_to="uploads/",
        verbose_name="главное изображение",
        blank=True,
        null=True,
    )

    is_on_main = django.db.models.BooleanField(default=False)

    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
    )

    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        editable=False,
        null=True,
    )

    def get_image_x300(self):

        return sorl.thumbnail.get_thumbnail(
            self.main_image,
            "300x300",
            crop="center",
            quality=100,
        )

    def image_tmb(self):
        if self.main_image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.main_image}' width='50'>",
            )

        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    list_display = "image_tmb"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]


class Gallery(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="uploads/",
        verbose_name="галлерея изоображений",
    )
    product = django.db.models.ForeignKey(
        "Item",
        on_delete=django.db.models.CASCADE,
        verbose_name="товар",
        related_name="galleries",
        related_query_name="gallery",
        blank=True,
    )

    def get_image_x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=100,
            format="PNG",
        )

    def image_tmb(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.image}' width='50'>",
            )

        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    list_display = "image_tmb"

    def __str__(self):
        return self.product.name[:15]


class Tag(core.models.AbstactModel):
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name="слаг",
        unique=True,
        help_text="Напишите slug",
        validators=[
            django.core.validators.RegexValidator(regex=r"^[a-zA-Z0-9_-]+$"),
        ],
    )

    normalform = django.db.models.CharField(
        editable=False,
        max_length=200,
        blank=True,
    )

    def clean(self):
        self.normalform = normalize_string(self.name)
        if Tag.objects.filter(normalform=self.normalform).exists():
            raise django.core.exceptions.ValidationError(
                "Похожий тег уже присутствует в базе данных",
            )

    def save(self, *args, **kwargs):
        if not self.normalform:
            self.normalform = normalize_string(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(core.models.AbstactModel):
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name="слаг",
        unique=True,
        help_text="Напишите slug",
        validators=[
            django.core.validators.RegexValidator(regex=r"^[a-zA-Z0-9_-]+$"),
        ],
    )
    weight = django.db.models.IntegerField(
        verbose_name="вес",
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text="Введите вес",
        default=100,
    )

    normalform = django.db.models.CharField(
        editable=False,
        max_length=200,
        blank=True,
    )

    def clean(self):
        self.normalform = normalize_string(self.name)
        if Category.objects.filter(normalform=self.normalform).exists():
            raise django.core.exceptions.ValidationError(
                "Похожая категория уже присутствует в базе данных",
            )

    def save(self, *args, **kwargs):
        if not self.normalform:
            self.normalform = normalize_string(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
