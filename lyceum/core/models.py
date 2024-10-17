import re

import django.core.exceptions
import django.db


def corr_name(value):
    value = re.sub(r'[^\w]', '', value).lower()
    target = 'abekmhopctyx'
    replacer = 'абекмнорстух'
    for i in range(len(value)):
        if value[i] in target:
            j = target.find(value[i])
            value = value.replace(target[j], replacer[j])
    return value


class AbstractModel(django.db.models.Model):
    id = django.db.models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='id',
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name='опубликовано',
        help_text='статус `опубликовано`',
    )
    name = django.db.models.CharField(
        max_length=150,
        unique=True,
        verbose_name='название',
        help_text='напишите сюда название',
    )

    class Meta:
        abstract = True


class NormName(AbstractModel):
    normalized_name = django.db.models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name='нормализованное имя',
    )

    class Meta:
        abstract = True

    def clean(self):
        self.normalized_name = corr_name(self.name)
        if (
            type(self)
            .objects.filter(normalized_name=self.normalized_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                'Такой элемент существует',
            )

    def save(self, *args, **kwargs):
        self.normalized_name = corr_name(self.name)
        return super().save(*args, **kwargs)
