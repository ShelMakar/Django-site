import django.core.validators
import django.db


class AbstractModel(django.db.models.Model):
    id = django.db.models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='id'
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name='опубликовано',
        help_text='статус `опубликовано`',
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name='название',
        help_text='напишите сюда название',
    )

    class Meta:
        abstract = True
