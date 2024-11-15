import django.conf
import django.contrib.auth.backends
import django.core.exceptions
import django.core.mail
import django.core.validators
import django.urls
import django.utils.encoding
import django.utils.http
import django.utils.timezone

import users.models
import users.tokens


class EmailBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            django.core.validators.validate_email(username)
            is_email = True
        except django.core.exceptions.ValidationError:
            is_email = False

        try:
            if is_email:
                try:
                    user = users.models.User.objects.by_mail(username)
                except users.models.User.DoesNotExist:
                    return None
            else:
                try:
                    user = users.models.User.objects.get(username=username)
                except users.models.User.DoesNotExist:
                    return None

            if user and user.check_password(password):
                profile, _ = users.models.Profile.objects.get_or_create(
                    user=user,
                )
                profile.attempts_count = 0
                profile.save()
                return user

            profile = users.models.Profile.objects.get(user=user)
            if (
                profile.attempts_count
                < int(django.conf.settings.MAX_AUTH_ATTEMPTS) - 1
            ):
                profile.attempts_count += 1
                profile.save()
            else:
                user.is_active = False
                profile.date_last_active = django.utils.timezone.now()
                user.save()
                profile.save()

                activation_path = django.urls.reverse(
                    'users:activate',
                    args=[
                        django.utils.http.urlsafe_base64_encode(
                            django.utils.encoding.force_bytes(user.pk),
                        ),
                        users.tokens.activation_token.make_token(user),
                    ],
                )
                confirmation_link = f'http://127.0.0.1:8000{activation_path}'

                django.core.mail.send_mail(
                    'Активация аккаунта',
                    f'Аккаунт заблокирован. '
                    f'Для того чтобы активировать свой аккаунт, '
                    f'нажмите на ссылку ниже (срок действия - 1 неделя): '
                    f'{confirmation_link}',
                    django.conf.settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

        except users.models.User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return users.models.User.objects.get(pk=user_id)
        except users.models.User.DoesNotExist:
            return None


__all__ = []
