from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from unittest import mock
from datetime import datetime, timedelta
from django.utils import timezone
import django.utils.http
import django.utils.encoding

from users.models import Profile
from users.token import account_activation_token

User = get_user_model()

class SignupTests(TestCase):
    def test_signup_creates_inactive_user_and_sends_email(self):
        response = self.client.post(reverse('users:signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!',
        })
        self.assertEqual(response.status_code, 200)  # Check if redirected or shows the message

        # Check that the user is created and is inactive
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)

        # Check if an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activation link has been sent to your email id', mail.outbox[0].subject)

class ActivationTests(TestCase):
    def setUp(self):
        # Создаем неактивного пользователя для активации
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.user.is_active = False
        self.user.save()

    @mock.patch('django.utils.timezone.now')
    def test_activate_user_within_time_limit(self, mock_now):
        # Мокаем текущее время на момент создания пользователя
        mock_now.return_value = timezone.now()
        uid = django.utils.http.urlsafe_base64_encode(django.utils.encoding.force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)

        # Пытаемся активировать пользователя в течение 12 часов
        response = self.client.get(reverse('users:activate', kwargs={'uidb64': uid, 'token': token}))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Thank you for your email confirmation', response.content.decode())

    @mock.patch('django.utils.timezone.now')
    def test_activation_link_expires_after_12_hours(self, mock_now):
        # Устанавливаем время на 13 часов после создания пользователя
        mock_now.return_value = timezone.now() + timedelta(hours=13)
        uid = django.utils.http.urlsafe_base64_encode(django.utils.encoding.force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)

        # Пробуем активировать по истекшей ссылке
        response = self.client.get(reverse('users:activate', kwargs={'uidb64': uid, 'token': token}))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Activation link has expired', response.content.decode())


class ProfileViewTests(TestCase):
    def setUp(self):
        # Создаем пользователя и логиним его
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password123')

    def test_profile_view_get(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_update(self):
        response = self.client.post(reverse('users:profile'), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
