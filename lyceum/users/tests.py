import datetime
import unittest.mock

import django.contrib.auth
import django.core.mail
import django.test
import django.urls
import django.utils.encoding
import django.utils.http
import django.utils.timezone

import users.models
import users.tokens

User = django.contrib.auth.get_user_model()


class SignupTests(django.test.TestCase):
    def test_signup_creates_inactive_user_and_sends_email(self):
        response = self.client.post(
            django.urls.reverse('users:signup'),
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'Testpassword123!',
                'password2': 'Testpassword123!',
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)
        self.assertEqual(len(django.core.mail.outbox), 1)
        self.assertIn(
            'Activation link has been sent to your email id',
            django.core.mail.outbox[0].subject,
        )


class ActivationTests(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )
        self.user.is_active = False
        self.user.save()

    @unittest.mock.patch('django.utils.timezone.now')
    def test_activate_user_within_time_limit(self, mock_now):
        mock_now.return_value = django.utils.timezone.now()
        uid = django.utils.http.urlsafe_base64_encode(
            django.utils.encoding.force_bytes(self.user.pk),
        )
        token = users.tokens.activation_token.make_token(self.user)
        response = self.client.get(
            django.urls.reverse(
                'users:activate', kwargs={'uidb64': uid, 'token': token},
            ),
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Thank you for your email confirmation',
            response.content.decode(),
        )

    @unittest.mock.patch('django.utils.timezone.now')
    def test_activation_link_expires_after_12_hours(self, mock_now):
        mock_now.return_value = (
            django.utils.timezone.now() + datetime.timedelta(hours=13)
        )

        uid = django.utils.http.urlsafe_base64_encode(
            django.utils.encoding.force_bytes(self.user.pk),
        )
        token = users.tokens.activation_token.make_token(self.user)

        response = self.client.get(
            django.urls.reverse(
                'users:activate', kwargs={'uidb64': uid, 'token': token},
            ),
        )
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Activation link has expired', response.content.decode())


class ProfileViewTests(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )
        self.profile = users.models.Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password123')

    def test_profile_view_get(self):
        response = self.client.get(django.urls.reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_update(self):
        response = self.client.post(
            django.urls.reverse('users:profile'),
            {
                'username': 'updateduser',
                'first_name': 'Updated',
                'last_name': 'User',
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')


__all__ = []
