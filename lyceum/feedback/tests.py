import shutil
import tempfile

import django.core.files.uploadedfile
import django.test
import django.urls


import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):

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
        # Set up a temporary directory for MEDIA_ROOT
        cls.test_media_root = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory after tests
        shutil.rmtree(cls.test_media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = django.test.Client()
        # Create a feedback instance for associating with uploaded files
        self.feedback = feedback.models.Feedback.objects.create(
            text='Test feedback',
        )

    def test_multiple_file_upload(self):
        feedback_data = {
            'text': 'Test feedback',
            'name': 'John Doe',
            'mail': 'johndoe@example.com',
        }

        # Create file upload instances
        file1 = django.core.files.uploadedfile.SimpleUploadedFile(
            'file1.txt',
            b'Content of file 1',
        )
        file2 = django.core.files.uploadedfile.SimpleUploadedFile(
            'file2.txt',
            b'Content of file 2',
        )

        # Combine all form data into a single POST request
        response = self.client.post(
            django.urls.reverse(
                'feedback:feedback',
            ),  # Adjust this to match your URL pattern
            {**feedback_data, 'file_field': [file1, file2]},
            follow=True,
        )

        # Check response status code and ensure redirect after form submission
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            django.urls.reverse('feedback:feedback'),
        )

        # Verify that the feedback instance was created
        feedback_count = feedback.models.Feedback.objects.count()
        self.assertEqual(
            feedback_count,
            2,
        )  # Adjust according to initial instances

        # Fetch the newly created feedback instance
        new_feedback = feedback.models.Feedback.objects.latest('created_on')

        # Verify that files are linked to the new feedback instance
        uploaded_files = feedback.models.FeedbackFile.objects.filter(
            feedback=new_feedback,
        )
        self.assertEqual(uploaded_files.count(), 2)

        # Validate the file paths
        file_names = [file.file.name for file in uploaded_files]
        self.assertIn(f'uploads/{new_feedback.id}/file1.txt', file_names)
        self.assertIn(f'uploads/{new_feedback.id}/file2.txt', file_names)


__all__ = ['FeedbackFormTests']
