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
    items = (
        catalog.models.Item.objects.filter(
            is_on_main=True,
            is_published=True,
            category__is_published=True,
        )
        .select_related('category')
        .prefetch_related(
            django.db.models.Prefetch(
                'tags',
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only('name'),
            ),
        )
        .only('name', 'text', 'id', 'category__name', 'main_image__item')
        .order_by('name')
    )
    context = {'items': items}
    return django.shortcuts.render(request, template, context)


__all__ = ['coffee', 'home']
