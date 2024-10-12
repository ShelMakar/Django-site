import http

import django.test

from parametrize import parametrize



class NumbersTest(django.test.TestCase):

    @parametrize('url', ['/catalog/', '/catalog/1/', '/catalog/re/4548878/'])
    def test_poz(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            'ошибка в тесте на ответ 200',
        )

    @parametrize(
        'url',
        [
            '/catalog/asasasasasa/',
            '/catalog/re/asasasasasa/',
            '/catalog/re/-45454/',
        ],
    )
    def test_neg(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.NOT_FOUND,
            'ошибка в тесте на ответ 404',
        )
