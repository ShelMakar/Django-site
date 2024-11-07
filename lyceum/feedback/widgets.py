import django.forms


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)


__all__ = ['MultipleFileField', 'MultipleFileInput']
