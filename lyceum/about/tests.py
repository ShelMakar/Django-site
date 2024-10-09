from unittest import TestCase


class NumbersTest(TestCase):

    def test_about(self):
        response = self.client.get('about/')
        self.assertEqual(response.status_code, 200, 'about feels bad')
