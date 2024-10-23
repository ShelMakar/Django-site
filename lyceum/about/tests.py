import http

import django.test
import django.urls


class NumbersTest(django.test.TestCase):

    def test_about(self):
        response = self.client.get(django.urls.reverse('about:description'))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            'about feels bad',
        )
