__all__ = []

import django.db


class AbstactModel(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Ввеедите название",
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Выберите, опубликовать ли товар?",
    )

    class Meta:
        abstract = True
