import django.test
import django.urls
import parameterized

import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):

    def setUp(self):
        self.url = django.urls.reverse('feedback:feedback')

    def test_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIsInstance(
            response.context['form'],
            feedback.forms.FeedbackForm,
        )

    @parameterized.parameterized.expand(
        [
            ('name', 'Имя', 'Как к вам обращаться?'),
            ('mail', 'Почта', 'Наишите Вашу почту'),
            ('text', 'Текст', 'Опишите обращение'),
        ],
    )
    def test_form_labels_and_help_texts(
        self,
        field_name,
        expected_label,
        expected_help_text,
    ):
        form = feedback.forms.FeedbackForm()
        self.assertEqual(form.fields[field_name].label, expected_label)
        self.assertEqual(form.fields[field_name].help_text, expected_help_text)

    def test_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            'name': 'Тест',
            'text': 'Тест',
            'mail': '123@l.com',
        }

        response = django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse('feedback:feedback'),
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )

        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                name='Тест',
                text='Тест',
                mail='123@l.com',
            ).exists(),
        )

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            'name': 'Тест',
            'text': 'Тест',
            'mail': 'notmail',
        }

        response = django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertTrue(response.context['form'].has_error('mail'))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )


__all__ = ['FeedbackFormTests']
