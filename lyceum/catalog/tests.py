__all__ = [
    "DinamicUrlTests",
    "DataBaseTests",
    "NormilizeStringTests",
    "ContextTests",
]

import http

import django.conf
import django.core.exceptions
import django.core.files.uploadedfile
import django.db.models.query
import django.test
import django.urls
import django.utils
import parametrize

import catalog.models
import lyceum.middleware


class DinamicUrlTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published_cateogory",
            weight=100,
        )

        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Опубликованный тег",
            slug="published_tag",
        )

        cls.published_item = catalog.models.Item.objects.create(
            is_published=True,
            name="Опубликованный товар",
            text="Превосходно",
            category=cls.published_category,
        )

        cls.published_category.save()
        cls.published_tag.save()
        cls.published_item.clean()
        cls.published_item.save()
        cls.published_item.tags.add(cls.published_tag.pk)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.published_category.delete()
        cls.published_item.delete()
        cls.published_tag.delete()

    @parametrize.parametrize(
        "url",
        [
            (django.urls.reverse("catalog:item_detail", args=[1])),
        ],
    )
    def test_endpoint_catalog_correct(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parametrize.parametrize("url", [("/catalog/string/"), ("/catalog/-1/")])
    def test_endpoint_catalog_uncorrect(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_endpoint_catalog_regular_correct(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:regular", args=[1]),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parametrize.parametrize(
        "url",
        [
            ("/catalog/re/-1/"),
            ("/catalog/re/test/"),
        ],
    )
    def test_endpoint_catalog_regular_uncorrect(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_endpoint_catalog_converter_correct(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:converter", args=[1]),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parametrize.parametrize(
        "url",
        [
            ("/catalog/converter/test/"),
            ("/catalog/converter/-1/"),
        ],
    )
    def test_endpoint_catalog_converter_uncorrect(self, url):
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_coffee_endpoint_text(self):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        response = django.test.Client().get(
            django.urls.reverse("homepage:coffee"),
        )
        self.assertIn("Я чайник", response.content.decode("utf-8"))

    @parametrize.parametrize(
        "url,answer",
        [
            (django.urls.reverse("catalog:item_list"), "косипС воравот"),
            (django.urls.reverse("catalog:item_detail", args=[1]), "равот"),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_russian_words_catalog_allow_true(
        self,
        url,
        answer,
    ):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        client = django.test.Client()
        for _ in range(9):
            response = client.get(url)
            self.assertNotIn(
                answer,
                bytes(response.content).decode("utf-8"),
            )

        response = client.get(url)
        self.assertIn(
            answer,
            bytes(response.content).decode("utf-8"),
        )

    @parametrize.parametrize(
        "url,answer",
        [
            (django.urls.reverse("catalog:item_list"), "косипС вотнемелэ"),
            (
                django.urls.reverse("catalog:item_detail", args=[12345]),
                "онбордоП тнемелэ",
            ),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_russian_words_catalog_allow_false(
        self,
        url,
        answer,
    ):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        client = django.test.Client()
        for _ in range(10):
            response = client.get(url)
            self.assertNotIn(
                answer,
                bytes(response.content).decode("utf-8"),
            )

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_russian_words_catalog_converter_true(self):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        client = django.test.Client()
        for _ in range(10):
            response = client.get(
                django.urls.reverse("catalog:converter", args=[12345]),
            )
            self.assertIn("12345", bytes(response.content).decode("utf-8"))

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_russian_words_catalog_converter_false(self):
        lyceum.middleware.MiddlewareReverseRussianWords.count = 0
        client = django.test.Client()
        for _ in range(10):
            response = client.get(
                django.urls.reverse("catalog:converter", args=[12345]),
            )
            self.assertNotIn("54321", bytes(response.content).decode("utf-8"))


class DataBaseTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = catalog.models.Category.objects.create(
            id=1,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            id=1,
            is_published=True,
            name="Тестовый тэг",
            slug="test-teg-slug",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tag.delete()
        cls.category.delete()

    def test_item_exsits_luxuriously_or_perfect(self):
        item_count = catalog.models.Item.objects.all().count()
        self.item = catalog.models.Item(
            name="Тестовое название",
            category=self.category,
            text="Тест роскошно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(DataBaseTests.tag)

        self.assertEqual(
            item_count + 1,
            catalog.models.Item.objects.all().count(),
        )

    def test_item_no_exsits_luxuriously_or_perfect(self):
        item_count = catalog.models.Item.objects.all().count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовое название",
                category=DataBaseTests.category,
                text="Нормальный тест",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(DataBaseTests.tag)

        self.assertEqual(item_count, catalog.models.Item.objects.all().count())

    def test_tag_slug(self):
        tag_count = catalog.models.Tag.objects.all().count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Tag(
                name="Тестовое название тега",
                slug="Слаг_тега",
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(tag_count, catalog.models.Tag.objects.all().count())

    def test_category_slug(self):
        category_count = catalog.models.Category.objects.all().count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Category(
                name="Тестовое название категории",
                slug="Слаг_категории",
                weight=100,
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            category_count,
            catalog.models.Category.objects.all().count(),
        )

    def test_category_weight_uncorrect(self):
        category_count = catalog.models.Category.objects.all().count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Category(
                name="Тестовое название категории",
                slug="test_slug",
                weight=0,
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            category_count,
            catalog.models.Category.objects.all().count(),
        )

    def test_category_weight_correct(self):
        category_count = catalog.models.Category.objects.all().count()
        self.item = catalog.models.Category(
            name="Тестовое название категории",
            slug="test_slug",
            weight=1,
        )
        self.item.full_clean()
        self.item.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Category.objects.all().count(),
        )


class NormilizeStringTests(django.test.TestCase):
    @parametrize.parametrize(
        "test_name1,test_slug1,test_name2,test_slug2",
        [
            ("tеstNаmе123", "first_slug", "Testname2", "second_slug"),
            (
                "теst__;№Наmе",
                "test_slug_first",
                "tеst_nаmе",
                "test_slug_second",
            ),
        ],
    )
    def test_tags_with_russian_letters(
        self,
        test_name1,
        test_slug1,
        test_name2,
        test_slug2,
    ):
        category_count = catalog.models.Tag.objects.all().count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(
                name=test_name1,
                slug=test_slug1,
            )
            self.tag.full_clean()
            self.tag.save()

            self.tag2 = catalog.models.Tag(
                name=test_name2,
                slug=test_slug2,
            )

            self.tag2.full_clean()
            self.tag2.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Tag.objects.all().count(),
        )

    @parametrize.parametrize(
        "test_name1,test_slug1,test_name2,test_slug2",
        [
            (
                "Test_normal_name",
                "normal_thirst_slug",
                "GoodTest",
                "normal_second_slug",
            ),
        ],
    )
    def test_tags_normal(self, test_name1, test_slug1, test_name2, test_slug2):
        category_count = catalog.models.Tag.objects.all().count()
        self.tag = catalog.models.Tag(
            name=test_name1,
            slug=test_slug1,
        )
        self.tag.full_clean()
        self.tag.save()

        self.tag2 = catalog.models.Tag(
            name=test_name2,
            slug=test_slug2,
        )

        self.tag2.full_clean()
        self.tag2.save()

        self.assertEqual(
            category_count + 2,
            catalog.models.Tag.objects.all().count(),
        )


class ContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published_category",
            weight=100,
        )

        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="Тестовая неопубликованная категория",
            slug="unpublished_category",
            weight=100,
        )

        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Опубликованный тег",
            slug="published_tag",
        )

        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="Неопубликованный тег",
            slug="unpublished_tag",
        )

        cls.published_item = catalog.models.Item.objects.create(
            is_published=True,
            name="Опубликованный товар",
            text="Превосходно",
            category=cls.published_category,
            is_on_main=True,
            created_at=django.utils.timezone.now(),
            updated_at=django.utils.timezone.now(),
        )

        cls.published_item_not_on_main = catalog.models.Item.objects.create(
            is_published=True,
            name="Опубликованный товар не на главной",
            text="Превосходно",
            category=cls.published_category,
            is_on_main=False,
            created_at=django.utils.timezone.now(),
            updated_at=django.utils.timezone.now(),
        )

        cls.unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            name="Неопубликованный товар",
            text="Превосходно",
            category=cls.published_category,
            is_on_main=True,
            created_at=django.utils.timezone.now(),
            updated_at=django.utils.timezone.now(),
        )

    @classmethod
    def tearDownClass(cls):
        cls.published_category.delete()
        cls.unpublished_category.delete()
        cls.published_item.delete()
        cls.unpublished_item.delete()
        cls.published_tag.delete()
        cls.unpublished_tag.delete()
        cls.published_item_not_on_main.delete()
        super().tearDownClass()

    def test_home_page_show_correct_context(self):
        response = self.client.get(django.urls.reverse("homepage:homepage"))
        self.assertIn("items", response.context)

    def test_home_page_count_item(self):
        response = self.client.get(django.urls.reverse("homepage:homepage"))
        self.assertEqual(len(response.context["items"]), 1)

    def test_home_page_type_context(self):
        response = self.client.get(django.urls.reverse("homepage:homepage"))
        self.assertIsInstance(
            response.context["items"],
            django.db.models.query.QuerySet,
        )

    def test_home_page_is_published_items(self):
        items = len(catalog.models.Item.objects.published())
        self.assertEqual(items, 2)

    def test_home_page_on_main_items(self):
        items = len(catalog.models.Item.objects.on_main())
        self.assertEqual(items, 1)

    def test_fileds_on_main(self):
        item = catalog.models.Item.objects.on_main().first()
        self.assertNotIn("is_published", item.__dict__)
        self.assertNotIn("MainImage", item.__dict__)
        self.assertNotIn("is_on_main", item.__dict__)
        self.assertIn("tags", item.__dict__["_prefetched_objects_cache"])

    def test_catalog_new_items(self):
        response = self.client.get(django.urls.reverse("catalog:new_items"))
        self.assertEqual(len(response.context["items"]), 2)

    def test_catalog_friday_items(self):
        response = self.client.get(django.urls.reverse("catalog:friday_items"))
        self.assertEqual(len(response.context["items"]), 0)

    def test_catalog_unverified_items(self):
        response = self.client.get(django.urls.reverse("catalog:unverified"))
        self.assertEqual(len(response.context["items"]), 2)
