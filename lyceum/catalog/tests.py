import http

import django.core.exceptions
import django.test
from parametrize import parametrize

import catalog.models


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
            catalog.models.Category.objects.count(), category_count,
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
            catalog.models.Category.objects.count(), category_count + 1,
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
