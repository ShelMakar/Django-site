import http

import django.test
import django.urls


class NumbersTest(django.test.TestCase):

    def test_homepage(self):
        response = self.client.get(django.urls.reverse('homepage:home'))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            'homepage feels bad',
        )

    def test_tea(self):
        response = self.client.get(django.urls.reverse('homepage:coffee'))

        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), 'Я чайник')


__all__ = ['NumbersTest']
