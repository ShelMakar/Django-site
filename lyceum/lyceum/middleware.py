import django.conf


class Middleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        Middleware.count += 1
        if str(django.conf.settings.ALLOW_REVERSE).lower() == 'false':
            return response

        if django.conf.settings.ALLOW_REVERSE:
            if Middleware.count % 10 == 0:

                def reverse(words):
                    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                    if len(words) != 0:
                        if words[0].lower() in alphabet:
                            return words[::-1]
                    return words

                word = response.content.decode().split(' ')
                response.content = ' '.join(map(reverse, word))
            return response
