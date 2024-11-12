import django.contrib.auth.models
import django.db


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='user',
        verbose_name='пользователь',
    )
    image = django.db.models.ImageField(
        upload_to='uploads/',
        verbose_name='аватарка',
        null=True,
        blank=True,
    )
    birthday = django.db.models.DateField(
        verbose_name='день рождения',
        null=True,
        blank=True,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name='счетчик кофе',
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


__all__ = []
