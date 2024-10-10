from django.test import Client, TestCase


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

    def test_return_string(self):
        response = Client().get('/catalog/re/asasasasasa/')
        self.assertEqual(response.status_code, 404, 'за строки карают')

    def test_return_not_int(self):
        response = Client().get('/catalog/re/-45454/')
        self.assertEqual(response.status_code, 404)

    def test_return_int(self):
        response = Client().get('/catalog/re/4548878/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, int(4548878))

    def test_converter_string(self):
        response = Client().get('/catalog/re/asasasasasa/')
        self.assertEqual(response.status_code, 404, 'за строки карают')

    def test_converter_not_int(self):
        response = Client().get('/catalog/re/-45454/')
        self.assertEqual(response.status_code, 404)

    def test_converter_int(self):
        response = Client().get('/catalog/re/4548878/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, int(4548878))
