import django.forms

import feedback.models
import feedback.widgets


class FileFieldForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.FeedbackFile
        fields = [feedback.models.FeedbackFile.file.field.name]
        widgets = {
            feedback.models.FeedbackFile.file.field.name:
                feedback.widgets.MultipleFileField(
                    label='Файлы', required=False,
                ),
        }


class FeedbackContactForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.FeedbackContact
        fields = [
            feedback.models.FeedbackContact.name.field.name,
            feedback.models.FeedbackContact.mail.field.name,
        ]
        labels = {
            feedback.models.FeedbackContact.name.field.name: 'Имя',
            feedback.models.FeedbackContact.mail.field.name: 'Почта',
        }
        help_texts = {
            feedback.models.FeedbackContact.name.field.name:
                'Как к вам обращаться?',
            feedback.models.FeedbackContact.mail.field.name:
                'Напишите Вашу почту',
        }
        widgets = {
            feedback.models.FeedbackContact.name.field.name:
                django.forms.TextInput(
                    attrs={'class': 'form-control'},
                ),
            feedback.models.FeedbackContact.mail.field.name:
                django.forms.EmailInput(
                    attrs={'class': 'form-control'},
                ),
        }


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = feedback.models.Feedback
        fields = [feedback.models.Feedback.text.field.name]
        labels = {
            feedback.models.Feedback.text.field.name: 'Текст обращения',
        }
        help_texts = {
            feedback.models.Feedback.text.field.name: 'Опишите ваше обращение',
        }
        widgets = {
            feedback.models.Feedback.text.field.name: django.forms.Textarea(
                attrs={'class': 'form-control'},
            ),
        }


__all__ = ['FeedbackForm']
