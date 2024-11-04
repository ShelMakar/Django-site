import http

import django.test
import django.urls
import parameterized

import lyceum.middleware


class EchoFormTests(django.test.TestCase):

    def setUp(self):
        self.form_url = django.urls.reverse('homepage:echo')
        self.submit_url = django.urls.reverse('homepage:echo_submit')

    def test_form_page_available(self):
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.context['form'].fields)

    def test_submit_page_only_post_allowed(self):
        response = self.client.get(self.submit_url)
        self.assertEqual(response.status_code, 405)

    @parameterized.parameterized.expand(
        [
            ('Hello, World!',),
            ('This is a test message.',),
            ('Тестовое сообщение.',),
        ],
    )
    def test_echo_submit(self, text_value):
        response = self.client.post(self.submit_url, {'text': text_value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), text_value)


class NumbersTest(django.test.TestCase):

    def test_homepage(self):
        response = self.client.get(django.urls.reverse('homepage:home'))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            'homepage feels bad',
        )

    def test_tea(self):
        lyceum.middleware.Middleware.count = 0
        response = self.client.get(django.urls.reverse('homepage:coffee'))

        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), 'Я чайник')


__all__ = ['NumbersTest']
