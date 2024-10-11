from . import settings


class Middleware:
    cnt = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.ALLOW_REVERSE or (settings.ALLOW_REVERSE is None):
            Middleware.cnt += 1
            if Middleware.cnt == 10:

                def reverse(words):
                    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                    if words[0].lower() in alphabet:
                        return words[::-1]
                    return words

                word = response.content.decode().split(' ')
                response.content = ' '.join(map(reverse, word))
                Middleware.cnt = 0

        return response
