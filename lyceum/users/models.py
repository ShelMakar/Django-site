import sys

import django.contrib.auth.models
import django.core.exceptions
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
    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name='счетчик попыток',
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class UserManager(django.contrib.auth.models.UserManager):

    def normalize_email(self, email, **kwargs):
        email = super().normalize_email(email)
        email = email.lower()
        local, domain = email.split('@', 1)
        if '+' in local:
            local = local[: local.index('+')]

        if domain == 'gmail.com':
            local = local.replace('.', '')

        if domain in ['ya.ru', 'yandex.ru']:
            domain = 'yandex.ru'
            local = '-'.join(local.split('.'))

        return f'{local}@{domain}'

    def active(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .select_related('profile')
        )

    def by_mail(self, login):
        normalized_email = UserManager.normalize_email(login)
        return self.active().get(email=normalized_email)


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def clean(self):
        self.normalized_email = UserManager.normalize_email(self.email)
        if (
            type(self)
            .objects.filter(normalized_email=self.normalized_email)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                'Пользователь с таким email уже существует.',
            )

    def save(self, *args, **kwargs):
        self.normalized_email = UserManager.normalize_email(self.email)
        return super().save(*args, **kwargs)


__all__ = []
