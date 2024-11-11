import http

import django.contrib.auth.decorators
import django.db
import django.http
import django.shortcuts

import catalog.models
import homepage.forms
import users.models


def coffee(request):
    if request.user.is_authenticated:
        profile = users.models.Profile.objects.get(user=request.user)
        profile.coffee_count += 1
        profile.save()

    return django.http.HttpResponse(
        'Я чайник',
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def echo(request):
    if request.method == 'GET':
        template = 'homepage/echo.html'
        form = homepage.forms.EchoForm(request.POST or None)
        context = {'form': form}
        return django.shortcuts.render(request, template, context)

    return django.http.HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


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
