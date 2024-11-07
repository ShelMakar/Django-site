import django.forms


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


__all__ = ['MultipleFileInput']
