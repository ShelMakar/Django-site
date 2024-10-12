import http

import django.test


class NumbersTest(django.test.TestCase):

    def test_homepage(self):
        response = django.teest.Client().get('/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK, 'homepage feels bad')

    def test_tea(self):
        response = django.test.Client().get('/coffee/')
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), 'Я чайник')
