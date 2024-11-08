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
    title = django.utils.translation.gettext('Пятница')
    items_queryset = catalog.models.Item.objects.published()
    friday_products = items_queryset.filter(updated_at__week_day=6).order_by(
        f'-{catalog.models.Item.updated_at.field.name}',
    )[:5]
    context = {'items': friday_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = 'catalog/unverified.html'

    one_sec = datetime.timedelta(seconds=1)

    unverified_products = catalog.models.Item.objects.published().filter(
        created_at__lte=django.db.models.F('updated_at') + one_sec,
    )

    title = django.utils.translation.gettext('Непроверенное')
    context = {'items': unverified_products, 'title': title}
    return django.shortcuts.render(request, template, context)


def new(request):
    template = 'catalog/new.html'
    title = django.utils.translation.gettext('Новинки')
    items_queryset = catalog.models.Item.objects.published()
    one_week_ago = django.utils.timezone.now() - datetime.timedelta(days=7)
    recent_products = items_queryset.filter(
        created_at__gte=one_week_ago,
    ).order_by('?')[:5]
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
