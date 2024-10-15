import http

import django.http


def home(request):
    return django.http.HttpResponse('<body>Главная</body>')


def tea(request):
    return django.http.HttpResponse(
        'Я чайник', status=http.HTTPStatus.IM_A_TEAPOT,
    )
