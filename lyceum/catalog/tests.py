import django.core.exceptions
import django.db
import django.test
import django.urls

# from parameterized import parameterized

import catalog.models


# class CatalogTest(django.test.TestCase):
#
#     @parameterized.expand(
#         [
#             ('catalog', django.urls.reverse('catalog:item_list'), 200),
#             (
#                 'catalog',
#                 django.urls.reverse('catalog:item_detail', args=[10]),
#                 200,
#             ),
#         ],
#     )
#     def test_catalog_endpoints(self, dont_used, url, expected):
#         response = django.test.Client().get(url)
#         self.assertEqual(
#             response.status_code,
#             expected,
#             'ошибка в тесте на ответ 200',
#         )


class ModelsTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name='тест категория',
            slug='test-category',
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='тест таг',
            slug='test-tag',
        )

    def test_not_correct_word(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Тестовый товар',
                category=self.category,
                text='нет нужного слова',
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    def test_correct_word(self):
        item_count = catalog.models.Item.objects.count()

        self.item = catalog.models.Item(
            name='Тестовый товар',
            category=self.category,
            text='роскошно',
        )
        self.item.full_clean()
        self.item.save()
        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)


class NormalTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name='Макар',
            slug='test-category',
            weight=100,
        )

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='тест',
            slug='test-tag',
        )
        cls.category_count = catalog.models.Category.objects.count()
        cls.tag_count = catalog.models.Tag.objects.count()

    def test_not_norm_category(self):
        category_count = self.category_count
        self.assertRaises(django.core.exceptions.ValidationError)
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    def test_not_norm_tag(self):
        tag_count = self.tag_count
        self.assertRaises(django.core.exceptions.ValidationError)
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count)

    def test_norm_category(self):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            is_published=True,
            name='тест категория',
            slug='test--category',
            weight=100,
        )
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    def test_norm_tag(self):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            is_published=True,
            name='тест таг',
            slug='test--tag',
        )
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)


class MediaTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_published = catalog.models.Category.objects.create(
            is_published=True,
            name='Тестовая опублик категория',
            slug='category_published',
            weight=50,
        )
        cls.category_unpublished = catalog.models.Category.objects.create(
            is_published=False,
            name='Тестовая неопублик категория',
            slug='category_unpublished',
            weight=50,
        )
        cls.tag_published = catalog.models.Tag.objects.create(
            is_published=True,
            name='Тестовая опублик тэг',
            slug='tag_published',
        )
        cls.tag_unpublished = catalog.models.Tag.objects.create(
            is_published=True,
            name='Тестовая неопублик тэг',
            slug='tag_unpublished',
        )
        cls.published_item = catalog.models.Item.objects.create(
            is_on_main=True,
            name='Тест опублик товар',
            category=cls.category_published,
            text='превосходно',
        )
        cls.unpublished_item = catalog.models.Item.objects.create(
            is_on_main=True,
            name='Тест неопублик товар',
            category=cls.category_unpublished,
            text='превосходно',
        )
        cls.tag_published.full_clean()
        cls.tag_published.save()
        cls.tag_unpublished.full_clean()
        cls.tag_unpublished.save()

        cls.category_unpublished.full_clean()
        cls.category_unpublished.save()
        cls.category_published.full_clean()
        cls.category_published.save()

        cls.published_item.full_clean()
        cls.published_item.save()
        cls.unpublished_item.full_clean()
        cls.unpublished_item.save()

        cls.published_item.tags.add(cls.tag_published.pk)
        cls.unpublished_item.tags.add(cls.tag_unpublished.pk)

    def test_homepage_shows_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse('homepage:home'),
        )
        items = response.context['items']
        self.assertIn('items', response.context)
        self.assertIsInstance(items, django.db.models.query.QuerySet)
        self.assertEqual(items.count(), 1)

    def test_catalog_shows_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse('catalog:item_list'),
        )
        items = response.context['items']
        self.assertIn('items', response.context)
        self.assertIsInstance(items, django.db.models.query.QuerySet)
        self.assertEqual(items.count(), 1)


__all__ = ['NormalTest', 'ModelsTest']
