from django.test import Client, TestCase
from django.test import override_settings


import lyceum.middleware


class ReverseWordsMiddlewareTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_none(self):
        lyceum.middleware.Middleware.count = 0
        for i in range(9):
            response = Client().get('/coffee/')
            self.assertEqual(response.content.decode(), 'Я чайник')
        response = Client().get('/coffee/')
        self.assertEqual(response.content.decode(), 'Я кинйач', 'True')

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_false(self):
        lyceum.middleware.Middleware.count = 0
        client = Client()
        for i in range(15):
            response = client.get('/coffee/')
            self.assertEqual(response.content.decode(), 'Я чайник', 'false')
