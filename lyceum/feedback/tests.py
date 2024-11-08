import shutil
import tempfile

import django.core.files.uploadedfile
import django.test
import django.urls


import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):
    def test_feedback_contact_form_labels_and_help_texts(self):
        form = feedback.forms.FeedbackContactForm()

        # Check labels
        self.assertEqual(form.fields['name'].label, 'Имя')
        self.assertEqual(form.fields['mail'].label, 'Почта')

        # Check help texts
        self.assertEqual(
            form.fields['name'].help_text,
            'Как к вам обращаться?',
        )
        self.assertEqual(form.fields['mail'].help_text, 'Напишите Вашу почту')

    def test_feedback_form_labels_and_help_texts(self):
        form = feedback.forms.FeedbackForm()

        # Check labels
        self.assertEqual(form.fields['text'].label, 'Текст обращения')

        # Check help texts
        self.assertEqual(
            form.fields['text'].help_text,
            'Опишите ваше обращение',
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
        self.assertTrue(response.context['user_form'].has_error('mail'))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )


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


@django.test.override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class MultipleFileUploadTest(django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_media_root = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory after tests
        shutil.rmtree(cls.test_media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = django.test.Client()
        self.feedback = feedback.models.Feedback.objects.create(
            text='Test feedback',
        )

    def test_multiple_file_upload(self):
        feedback_data = {
            'text': 'Test feedback',
            'name': 'John Doe',
            'mail': 'johndoe@example.com',
        }
        file1 = django.core.files.uploadedfile.SimpleUploadedFile(
            'file1.txt',
            b'Content of file 1',
        )
        file2 = django.core.files.uploadedfile.SimpleUploadedFile(
            'file2.txt',
            b'Content of file 2',
        )
        response = self.client.post(
            django.urls.reverse(
                'feedback:feedback',
            ),
            {**feedback_data, 'file_field': [file1, file2]},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            django.urls.reverse('feedback:feedback'),
        )
        feedback_count = feedback.models.Feedback.objects.count()
        self.assertEqual(
            feedback_count,
            2,
        )
        new_feedback = feedback.models.Feedback.objects.latest('created_on')
        uploaded_files = feedback.models.FeedbackFile.objects.filter(
            feedback=new_feedback,
        )
        self.assertEqual(uploaded_files.count(), 2)
        file_names = [file.file.name for file in uploaded_files]
        self.assertIn(f'uploads/{new_feedback.id}/file1.txt', file_names)
        self.assertIn(f'uploads/{new_feedback.id}/file2.txt', file_names)


__all__ = ['FeedbackFormTests']
