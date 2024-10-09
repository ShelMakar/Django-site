from unittest import TestCase


class NumbersTest(TestCase):

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200, 'homepage feels bad')
