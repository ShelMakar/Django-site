from django.test import Client, TestCase, override_settings
import django.conf

from lyceum.middleware import Middleware


class ReverseWordsMiddlewareTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_none(self):
        Middleware.cnt = 0
        for i in range(9):
            response = Client().get('/coffee/')
            self.assertEqual(response.content.decode(), 'Я чайник')
        response = Client().get('/coffee/')
        self.assertEqual(response.content.decode(), 'Я кинйач', 'True')

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_false(self):
        Middleware.cnt = 0
        client = Client()
        print(django.conf.settings.ALLOW_REVERSE)
        for i in range(15):
            response = client.get('/coffee/')
            self.assertEqual(response.content.decode(), 'Я чайник', 'false')

