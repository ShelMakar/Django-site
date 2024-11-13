import sys

import django.contrib.auth.models
import django.db


if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    User = django.contrib.auth.models.User
    email_field = User._meta.get_field('email')
    email_field._unique = True


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


class UserManager(django.db.models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def active(self):
        return self.get_queryset().get(is_active=True)

    def by_mail(self, email):
        return self.get_queryset().get(email=email)


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


__all__ = []
