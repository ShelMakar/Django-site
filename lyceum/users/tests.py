from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserAuthorizationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
        )

    def test_login_with_valid_credentials(self):
        login_successful = self.client.login(
            username='testuser', password='password123',
        )
        self.assertTrue(
            login_successful,
            'Пользователь должен иметь возможность'
            ' войти в систему с правильными учетными данными',
        )

    def test_login_with_invalid_credentials(self):
        login_successful = self.client.login(
            username='testuser', password='wrongpassword',
        )
        self.assertFalse(
            login_successful,
            'Пользователь не должен иметь возможности'
            ' войти в систему с неверными учетными данными',
        )

    def test_logout(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(
            response,
            reverse('users:login'),
            msg_prefix='Пользователь должен быть перенаправлен'
                       ' на страницу входа в систему после выхода из системы',
        )
        response = self.client.get(reverse('homepage:home'))
        self.assertNotContains(
            response,
            'Logout',
            msg_prefix='Ссылка для выхода из системы не должна'
                       ' отображаться для вышедших из системы пользователей',
        )


__all__ = []
