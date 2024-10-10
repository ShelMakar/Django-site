from django.test import Client, TestCase


class NumbersTest(TestCase):

    def test_homepage(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200, 'homepage feels bad')

    def test_tea(self):
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode(), '<body>Я чайник</body>')
