from unittest import TestCase


class NumbersTest(TestCase):

    def test_catalog(self):
        response = self.client.get('catalog/')
        self.assertEqual(response.status_code, 200, 'ошибка')

    def test_catalog_int(self):
        response = self.client.get('catalog/1')
        self.assertEqual(response.status_code, 200, 'нельзя не число')

    def test_catalog_not_int(self):
        response = self.client.get('catalog/asasasasasa')
        self.assertNotEqual(response.status_code, 404, 'за строки карают')
