from http import HTTPStatus
import django.http


def home(request):
    return django.http.HttpResponse('<body>Главная</body>')


def tea(request):
    return django.http.HttpResponse(
        '<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT
    )
