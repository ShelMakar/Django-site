from django.test import TestCase, Client


class NumbersTest(TestCase):

    def test_homepage(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200, 'homepage feels bad')
