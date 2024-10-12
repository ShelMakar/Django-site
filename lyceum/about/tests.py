import http

import django.test


class NumbersTest(django.test.TestCase):

    def test_about(self):
        response = django.test.Client().get('/about/')
        self.assertEqual(
            response.status_code, http.HTTPStatus.OK, 'about feels bad'
        )
