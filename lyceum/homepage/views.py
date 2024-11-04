import http

import django.db
import django.http
import django.shortcuts

import catalog.models
import homepage.forms


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


def echo(request):
    template = 'homepage/echo.html'
    form = homepage.forms.EchoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        context = {'form': form}
        return django.shortcuts.render(request, template, context)

    return django.http.HttpResponseNotAllowed(['POST'])


def echo_submit(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        return django.http.HttpResponse(text)

    return django.http.HttpResponseNotAllowed(['POST'])


def home(request):
    template = 'homepage/main.html'
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return django.shortcuts.render(request, template, context)


__all__ = ['coffee', 'home']
