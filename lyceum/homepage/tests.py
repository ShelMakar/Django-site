from http import HTTPStatus

from django.test import Client, TestCase


class NumbersTest(TestCase):

    def test_homepage(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200, 'homepage feels bad')

    def test_tea(self):
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), 'Я чайник')
