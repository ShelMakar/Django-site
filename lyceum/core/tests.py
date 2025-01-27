__all__ = []

import datetime
import unittest.mock
import zoneinfo

import django.test
import django.urls
import django.utils.timezone

import users.models


class BirthdayUsersMixinTestCase(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user1 = users.models.User.objects.create(
            username="user1",
            email="user1@example.com",
        )
        cls.user2 = users.models.User.objects.create(
            username="user2",
            email="user2@example.com",
        )
        cls.user3 = users.models.User.objects.create(
            username="user3",
            email="user3@example.com",
        )

        cls.birthday_in_moscow = django.utils.timezone.datetime(2024, 11, 1)

        today = django.utils.timezone.localdate(django.utils.timezone.now())
        yesterday = today - datetime.timedelta(days=1)

        users.models.Profile.objects.update_or_create(
            user=cls.user1,
            defaults={"birthday": today},
        )
        users.models.Profile.objects.update_or_create(
            user=cls.user2,
            defaults={"birthday": yesterday},
        )
        users.models.Profile.objects.update_or_create(
            user=cls.user3,
            defaults={"birthday": cls.birthday_in_moscow},
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user1.delete()
        cls.user2.delete()
        cls.user3.delete()

    def test_get_context_data(self):

        request = self.client.get(django.urls.reverse("homepage:homepage"))

        self.assertIn("birthday", request.context)

        birthday_list = request.context["birthday"]

        self.assertEqual(len(birthday_list), 1)
        self.assertEqual(birthday_list[0]["username"], "user1")
        self.assertEqual(birthday_list[0]["email"], "user1@example.com")

    def test_get_correct_data_in_different_template(self):

        request_one = self.client.get(django.urls.reverse("about:about"))

        self.assertIn("birthday", request_one.context)
        self.assertEqual(len(request_one.context["birthday"]), 1)
        self.assertEqual(
            request_one.context["birthday"][0]["username"],
            "user1",
        )
        self.assertEqual(
            request_one.context["birthday"][0]["email"],
            "user1@example.com",
        )

    def test_another_get_correct_data_in_different_template(self):

        request_two = self.client.get(django.urls.reverse("users:login"))

        self.assertIn("birthday", request_two.context)
        self.assertEqual(len(request_two.context["birthday"]), 1)
        self.assertEqual(
            request_two.context["birthday"][0]["username"],
            "user1",
        )
        self.assertEqual(
            request_two.context["birthday"][0]["email"],
            "user1@example.com",
        )

    def test_correct_fields(self):
        request = self.client.get(django.urls.reverse("homepage:homepage"))

        self.assertNotIn("coffee_count", request.context.__dict__)
        self.assertNotIn("image", request.context.__dict__)
        self.assertNotIn("attempts_count", request.context.__dict__)

    def test_birthday_in_timezones(self):
        mock_now = datetime.datetime(
            2024,
            10,
            31,
            23,
            30,
            tzinfo=django.utils.timezone.utc,
        )

        with unittest.mock.patch(
            "django.utils.timezone.now",
            return_value=mock_now,
        ):
            # Europe/Moscow
            response_moscow = self.client.get(
                django.urls.reverse("homepage:homepage"),
                HTTP_COOKIE="django_timezone=Europe/Moscow",
            )

            user_timezone = zoneinfo.ZoneInfo("Europe/Moscow")
            local_today_moscow = django.utils.timezone.localdate(
                mock_now.astimezone(user_timezone),
            )

            self.assertEqual(local_today_moscow, datetime.date(2024, 11, 1))
            self.assertIn("birthday", response_moscow.context)

            birthday_list_moscow = response_moscow.context["birthday"]
            self.assertEqual(len(birthday_list_moscow), 1)
            self.assertEqual(birthday_list_moscow[0]["username"], "user3")

            # UTC
            response_utc = self.client.get(
                django.urls.reverse("homepage:homepage"),
                HTTP_COOKIE="django_timezone=UTC",
            )

            local_today_utc = django.utils.timezone.localdate(mock_now)
            self.assertEqual(local_today_utc, datetime.date(2024, 10, 31))
            self.assertIn("birthday", response_utc.context)

            birthday_list_utc = response_utc.context["birthday"]
            self.assertEqual(len(birthday_list_utc), 0)

    def test_context_processor_with_no_birthdays(self):
        mock_today = django.utils.timezone.localdate(
            django.utils.timezone.now(),
        ) + datetime.timedelta(days=7)

        with unittest.mock.patch(
            "django.utils.timezone.localdate",
            return_value=mock_today,
        ):
            response = self.client.get(
                django.urls.reverse("homepage:homepage"),
            )
            self.assertIn("birthday", response.context)

            birthday_list = response.context["birthday"]
            self.assertEqual(len(birthday_list), 0)

    def test_timezone_cookie_handling(self):
        self.client.get(
            django.urls.reverse("homepage:homepage"),
            HTTP_COOKIE="django_timezone=Europe/Moscow",
        )
        timezone = django.utils.timezone.get_current_timezone()
        self.assertEqual(timezone, zoneinfo.ZoneInfo("Europe/Moscow"))

        self.client.get(django.urls.reverse("homepage:homepage"))
        timezone = django.utils.timezone.get_current_timezone()
        self.assertEqual(timezone, zoneinfo.ZoneInfo("UTC"))
