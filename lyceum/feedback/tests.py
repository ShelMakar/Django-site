import django.test
import django.urls
import parameterized

from feedback.forms import FeedbackForm


class FeedbackFormTests(django.test.TestCase):

    def setUp(self):
        self.url = django.urls.reverse('feedback:feedback')

    def test_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], FeedbackForm)

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
        form = FeedbackForm()
        self.assertEqual(form.fields[field_name].label, expected_label)
        self.assertEqual(form.fields[field_name].help_text, expected_help_text)

    def test_redirect(self):
        response = self.client.post(
            self.url,
            {
                'name': 'Тестовое имя',
                'mail': 'test@example.com',
                'text': 'Это тестовое сообщение',
            },
        )
        self.assertRedirects(response, self.url)


__all__ = ['FeedbackFormTests']
