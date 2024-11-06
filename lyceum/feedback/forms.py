import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = feedback.models.Feedback
        fields = '__all__'
        exclude = ['created_on', 'status']

        labels = {
            feedback.models.Feedback.name.field.name: 'Имя',
            feedback.models.Feedback.text.field.name: 'Текст',
            feedback.models.Feedback.mail.field.name: 'Почта',
        }

        help_texts = {
            feedback.models.Feedback.name.field.name: 'Как к вам обращаться?',
            feedback.models.Feedback.text.field.name: 'Опишите обращение',
            feedback.models.Feedback.mail.field.name: 'Наишите Вашу почту',
        }


__all__ = ['FeedbackForm']
