import re

import django.conf


class Middleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not django.conf.settings.ALLOW_REVERSE:
            return False

        cls.count += 1
        if cls.count % 10 != 0:
            return False

        cls.count = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode()

        reversed_content = re.sub(
            r'\b[а-яА-ЯёЁ]+\b',
            lambda match: match.group(0)[::-1],
            content,
        )

        response.content = reversed_content.encode()
        return response


__all__ = ['Middleware']
