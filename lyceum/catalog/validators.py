import re

import django.core.validators
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomValidator:
    def __init__(self, *args):
        self.args = args

    def __eq__(self, other):
        return self.args == other.args

    def __call__(self, value):
        words = value.lower().split()
        for word in words:
            for corr_word in self.args:
                pat = re.compile(r'\b' + corr_word + r'\b')
                if re.search(pat, word):
                    return

        raise django.core.validators.ValidationError(
            f'{value} не содержит слов `роскошно` или `превосходно`',
        )


__all__ = ['CustomValidator']
