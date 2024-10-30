import http

import django.db
import django.http
import django.shortcuts

import catalog.models


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
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return django.shortcuts.render(request, template, context)


__all__ = ['coffee', 'home']
