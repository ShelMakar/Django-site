import django.conf
import django.contrib.auth
import django.core.mail
import django.test
import django.urls
import django.utils.encoding
import django.utils.http
import django.utils.timezone
import parametrize

import users.models
import users.tokens

User = django.contrib.auth.get_user_model()


class UserAuthorizationTests(django.test.TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
        )
        users.models.Profile.objects.create(user=self.user)

    def test_login_with_valid_credentials(self):
        login_successful = self.client.login(
            username='testuser',
            password='password123',
        )
        self.assertTrue(
            login_successful,
            'Пользователь должен иметь возможность'
            ' войти в систему с правильными учетными данными',
        )

    def test_login_with_invalid_credentials(self):
        login_successful = self.client.login(
            username='testuser',
            password='wrongpassword',
        )
        self.assertFalse(
            login_successful,
            'Пользователь не должен иметь возможности'
            ' войти в систему с неверными учетными данными',
        )

    def test_logout(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.get(django.urls.reverse('users:logout'))
        self.assertRedirects(
            response,
            django.urls.reverse('users:login'),
            msg_prefix='Пользователь должен быть перенаправлен'
            ' на страницу входа в систему после выхода из системы',
        )
        response = self.client.get(django.urls.reverse('homepage:home'))
        self.assertNotContains(
            response,
            'Logout',
            msg_prefix='Ссылка для выхода из системы не должна'
            ' отображаться для вышедших из системы пользователей',
        )


@django.test.override_settings(
    ALLOW_REVERSE=False,
    DEFAULT_USER_IS_ACTIVE=True,
)
class EmailNormalizeTests(django.test.TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        self.django_user = User.objects.create_user(
            **self.user_data,
        )
        self.normalizer = users.models.UserManager()

    @parametrize.parametrize(
        'input_email, expected',
        [
            ('user@example.com', 'user@example.com'),
            ('User@Example.COM', 'user@example.com'),
            ('user@yandex.ru', 'user@yandex.ru'),
            ('user@ya.ru', 'user@yandex.ru'),
            ('user@gmail.com', 'user@gmail.com'),
            ('username+spam@gmail.com', 'username@gmail.com'),
            ('user.name+spam@gmail.com', 'username@gmail.com'),
            ('username+whatever@gmail.com', 'username@gmail.com'),
            ('user.name@gmail.com', 'username@gmail.com'),
            ('u.s.e.r.n.a.m.e@gmail.com', 'username@gmail.com'),
            ('user@outlook.com', 'user@outlook.com'),
        ],
    )
    def test_normalize(self, input_email, expected):
        normal = self.normalizer.normalize_email(input_email)
        self.assertEqual(normal, expected)


class EmailBackendTestCase(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            is_active=True,
        )
        self.profile = users.models.Profile.objects.create(
            user=self.user,
            attempts_count=0,
        )

        django.conf.settings.MAX_AUTH_ATTEMPTS = 3

    def test_user_block_after_max_attempts(self):
        for _ in range(django.conf.settings.MAX_AUTH_ATTEMPTS):
            self.client.login(username='testuser', password='wrongpassword')

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertFalse(self.user.is_active)
        self.assertEqual(
            self.profile.attempts_count,
            django.conf.settings.MAX_AUTH_ATTEMPTS - 1,
        )

        self.assertEqual(len(django.core.mail.outbox), 1)
        self.assertIn('Активация аккаунта', django.core.mail.outbox[0].subject)
        self.assertIn(
            'Замечена подозрительная активность аккаунта',
            django.core.mail.outbox[0].body,
        )

    def test_user_reactivation(self):
        self.profile.attempts_count = django.conf.settings.MAX_AUTH_ATTEMPTS
        self.user.is_active = False
        self.user.date_joined = django.utils.timezone.now()
        self.user.save()
        self.profile.save()

        uid = django.utils.http.urlsafe_base64_encode(
            django.utils.encoding.force_bytes(self.user.pk),
        )
        token = users.tokens.activation_token.make_token(self.user)
        activation_url = django.urls.reverse(
            'users:activate',
            args=[uid, token],
        )

        response = self.client.get(activation_url)

        self.user.refresh_from_db()

        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Thank you for your email confirmation',
            response.content.decode(),
        )


__all__ = []
