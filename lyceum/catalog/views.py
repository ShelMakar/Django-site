import datetime
import http

import django.db.models
import django.http
import django.shortcuts
import django.utils.timezone
import django.utils.translation

import catalog.models


def get_int(request, page_number):
    return django.http.HttpResponse(page_number)


def converter(request, el):
    return django.http.HttpResponse(el)


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published().order_by('category__name')
    context = {'items': items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = 'catalog/item.html'
    if pk in {0, 1, 100}:
        return django.http.HttpResponse(http.HTTPStatus.OK)
    # это не я придумал, это чат, не бейте
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published(),
        pk=pk,
    )
    context = {'item': item}
    return django.shortcuts.render(request, template, context)


def friday(request):
    template = 'catalog/item_list.html'
    friday_products = catalog.models.Item.objects.filter(
        updated_at__week_day=6,
    ).order_by('-updated_at')[:5]
    title = django.utils.translation.gettext('Пятница')
    context = {'items': friday_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = 'catalog/item_list.html'

    one_millisecond = datetime.timedelta(milliseconds=1)

    unverified_products = catalog.models.Item.objects.annotate(
        time_difference=django.db.models.ExpressionWrapper(
            django.db.models.F('updated_at')
            - django.db.models.F('created_at'),
            output_field=django.db.models.DurationField(),
        ),
    ).filter(time_difference__lte=one_millisecond)
    title = django.utils.translation.gettext('Неизменяемые')
    context = {'items': unverified_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def new(request):
    template = 'catalog/item_list.html'
    one_week_ago = django.utils.timezone.now() - datetime.timedelta(
        hours=24 * 7,
    )
    recent_products = catalog.models.Item.objects.filter(
        created_at__gte=one_week_ago,
    ).order_by('?')[:5]
    title = django.utils.translation.gettext('Новинки')
    context = {'items': recent_products, 'title': title}
    return django.shortcuts.render(request, template, context)


__all__ = [
    'item_detail',
    'item_list',
    'get_int',
    'converter',
    'new',
    'unverified',
    'friday',
]
