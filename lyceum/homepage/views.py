import http

import django.http
import django.shortcuts


def coffee(request):
    return django.http.HttpResponse(
        'Я чайник',
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def tea1(request):
    template = 'homepage/main.html'
    context = {}
    return django.shortcuts.render(
        request,
        template,
        context,
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def home(request):
    template = 'homepage/main.html'
    context = {
        'out': [
            {
                'id': 1,
                'name': 'Куриная шаурма',
                'text': 'Блаженство, включающее в себя мясо курицы.',
                'img': 'chiken_shav.jpg',
            },
            {
                'id': 2,
                'name': 'Хачапури по-аджарски',
                'text': 'Блаженство, включающее в себя мясо курицы.',
                'img': 'Danila.jpg',
            },
            {
                'id': 3,
                'name': 'Шашлык из барашка',
                'text': 'Блаженство, включающее в себя мясо курицы.',
                'img': 'shashlyck_baran.jpg',
            },
        ],
    }
    return django.shortcuts.render(request, template, context)
