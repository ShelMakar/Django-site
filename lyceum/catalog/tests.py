from django.test import TestCase, Client


class NumbersTest(TestCase):

    def test_catalog(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200, 'ошибка')

    def test_catalog_int(self):
        response = Client().get('/catalog/1/')
        self.assertEqual(response.status_code, 200, 'нельзя не число')

    def test_catalog_not_int(self):
        response = Client().get('/catalog/asasasasasa/')
        self.assertEqual(response.status_code, 404, 'за строки карают')
