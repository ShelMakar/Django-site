from django.test import TestCase, Client, override_settings


class ReverseWordsMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_none(self):
        client = Client()
        for i in range(9):
            response = client.get('/coffee/')
            self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
        response = client.get('/coffee/')
        self.assertEqual(response.content.decode('utf-8'), 'Я кинйач')

    @override_settings(ALLOW_REVERSE=None)
    def test_middleware_none(self):
        client = Client()
        for i in range(9):
            response = client.get('/coffee/')
            self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
        response = client.get('/coffee/')
        self.assertEqual(response.content.decode('utf-8'), 'Я кинйач')

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_false(self):
        client = Client()
        for i in range(9):
            response = client.get('/coffee/')
            self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
        response = client.get('/coffee/')
        self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
