import datetime

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
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published(),
        pk=pk,
    )
    context = {'item': item}
    return django.shortcuts.render(request, template, context)


def friday(request):
    template = 'catalog/friday.html'
    friday_products = (
        catalog.models.Item.objects.published()
        .filter(
            updated_at__week_day=6,
        )
        .order_by('-updated_at')[:5]
    )
    title = django.utils.translation.gettext('Пятница')
    context = {'items': friday_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = 'catalog/unverified.html'

    unverified_products = catalog.models.Item.objects.published().filter(
        created_at__lt=django.db.models.F('updated_at')
    )

    title = django.utils.translation.gettext('Неизменяемые')
    context = {'items': unverified_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def new(request):
    template = 'catalog/new.html'
    one_week_ago = django.utils.timezone.now() - datetime.timedelta(
        hours=24 * 7,
    )
    recent_products = (
        catalog.models.Item.objects.published()
        .filter(
            created_at__gte=one_week_ago,
        )
        .order_by('?')[:5]
    )
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
