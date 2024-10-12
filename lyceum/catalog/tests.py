import http

import django.test


class NumbersTest(django.test.TestCase):

    def test_catalog(self):
        response = django.test.Client().get('/catalog/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK, 'ошибка')

    def test_catalog_int(self):
        response = django.test.Client().get('/catalog/1/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK, 'нельзя не число')

    def test_catalog_not_int(self):
        response = django.test.Client().get('/catalog/asasasasasa/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND, 'за строки карают')

    def test_return_string(self):
        response = django.test.Client().get('/catalog/re/asasasasasa/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND, 'за строки карают')

    def test_return_not_int(self):
        response = django.test.Client().get('/catalog/re/-45454/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_return_int(self):
        response = django.test.Client().get('/catalog/re/4548878/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, int(4548878))

    def test_converter_string(self):
        response = django.test.Client().get('/catalog/re/asasasasasa/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND, 'за строки карают')

    def test_converter_not_int(self):
        response = django.test.Client().get('/catalog/re/-45454/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_converter_int(self):
        response = django.test.Client().get('/catalog/re/4548878/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, int(4548878))
