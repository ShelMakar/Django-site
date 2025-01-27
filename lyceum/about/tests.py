__all__ = [
    "StaticUrlTests",
]
import http

import django.test

import lyceum.middleware


class StaticUrlTests(django.test.TestCase):
    def test_about_endpoint(self):
        response = django.test.Client().get(django.urls.reverse("about:about"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "status code != 200",
        )

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_russian_about_allow_reverse_true(self):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        client = django.test.Client()
        for _ in range(9):
            response = client.get(django.urls.reverse("about:about"))
            self.assertNotIn(
                "О еткеорп",
                bytes(response.content).decode("utf-8"),
            )

        response = client.get(django.urls.reverse("about:about"))
        self.assertIn("О еткеорп", bytes(response.content).decode("utf-8"))

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_russian_about_allow_reverse_false(self):
        client = django.test.Client()
        for _ in range(10):
            response = client.get(django.urls.reverse("about:about"))
            self.assertNotIn(
                "О еткеорп",
                bytes(response.content).decode("utf-8"),
            )
