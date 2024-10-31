import datetime

import django.core.exceptions
import django.db
import django.test
import django.urls
import django.utils.timezone

import catalog.models


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
    fixtures = ['fixtures/data.json']

    def test_homepage_shows_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse('homepage:home'),
        )
        items = response.context['items']
        self.assertIsInstance(items, django.db.models.query.QuerySet)
        self.assertEqual(len(items), 3)

    def test_homepage_shows_len(self):
        response = django.test.Client().get(
            django.urls.reverse('homepage:home'),
        )
        self.assertIn('items', response.context)

    def test_catalog_shows_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse('catalog:item_list'),
        )
        items = response.context['items']
        self.assertIsInstance(items, django.db.models.query.QuerySet)
        self.assertEqual(len(items), 5)

    def test_catalog_shows_len(self):
        response = django.test.Client().get(
            django.urls.reverse('catalog:item_list'),
        )
        self.assertIn('items', response.context)

    def test_catalog_fields(self):
        response = django.test.Client().get(
            django.urls.reverse('catalog:item_list'),
        )
        self.assertIn(
            'tags',
            response.context['items'][0]._prefetched_objects_cache,
        )

    def test_homepage_fields(self):
        response = django.test.Client().get(
            django.urls.reverse('homepage:home'),
        )
        self.assertIn(
            'tags',
            response.context['items'][0]._prefetched_objects_cache,
        )

    def test_category(self):
        item = catalog.models.Item.objects.published().first().__dict__
        self.assertIn('category_id', item)
        self.assertNotIn('is_published', item)
        self.assertIn('text', item)
        self.assertIn('name', item)

    def test_homepage(self):
        item = catalog.models.Item.objects.on_main().first().__dict__
        self.assertIn('category_id', item)
        self.assertNotIn('is_published', item)
        self.assertIn('text', item)
        self.assertIn('name', item)
        self.assertNotIn('is_on_main', item)


class DataTimeTest(django.test.TestCase):
    def test_view_url_exists_new(self):
        response = self.client.get(django.urls.reverse('catalog:new'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_new(self):
        response = self.client.get(django.urls.reverse('catalog:new'))
        self.assertTemplateUsed(response, 'catalog/item_list.html')

    def test_view_returns_recent_products_new(self):
        response = self.client.get(django.urls.reverse('catalog:new'))
        recent_products = response.context['items']

        one_week_ago = django.utils.timezone.now() - datetime.timedelta(days=7)
        for product in recent_products:
            self.assertGreaterEqual(product.created_at, one_week_ago)

    def test_view_returns_maximum_five_products_new(self):
        response = self.client.get(django.urls.reverse('catalog:new'))
        self.assertLessEqual(len(response.context['items']), 5)

    def test_view_url_exists_friday(self):
        response = self.client.get(django.urls.reverse('catalog:friday'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_friday(self):
        response = self.client.get(django.urls.reverse('catalog:friday'))
        self.assertTemplateUsed(response, 'catalog/item_list.html')

    def test_view_returns_only_friday_products_friday(self):
        response = self.client.get(django.urls.reverse('catalog:friday'))
        friday_products = response.context['items']
        for product in friday_products:
            self.assertEqual(product.updated_at.weekday(), 6)

    def test_view_returns_maximum_five_products_friday(self):
        response = self.client.get(django.urls.reverse('catalog:friday'))
        self.assertLessEqual(len(response.context['items']), 5)

    def test_view_url_exists_unverified(self):
        response = self.client.get(django.urls.reverse('catalog:unverified'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_unverified(self):
        response = self.client.get(django.urls.reverse('catalog:unverified'))
        self.assertTemplateUsed(response, 'catalog/item_list.html')

    def test_view_returns_only_unverified_product_unverified(self):
        response = self.client.get(django.urls.reverse('catalog:unverified'))
        unverified_products = response.context['items']
        for product in unverified_products:
            self.assertEqual(product.created_at, product.updated_at)


__all__ = ['NormalTest', 'ModelsTest']
