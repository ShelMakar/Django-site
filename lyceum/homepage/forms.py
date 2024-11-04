import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        label='Напишите текст',
        max_length=100,
    )


__all__ = ['EchoForm']
