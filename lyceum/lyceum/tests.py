import django.test
import django.urls

import lyceum.middleware


class ReverseWordsMiddlewareTests(django.test.TestCase):

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_middleware_none(self):
        lyceum.middleware.Middleware.count = 0
        for i in range(9):
            response = django.urls.reverse('coffee')
            self.assertEqual(response.content.decode(), 'Я чайник')
        response = django.urls.reverse('coffee')
        self.assertEqual(response.content.decode(), 'Я кинйач', 'True')

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_middleware_false(self):
        lyceum.middleware.Middleware.count = 0
        for i in range(15):
            response = django.urls.reverse('coffee')
            self.assertEqual(response.content.decode(), 'Я чайник', 'false')
