import django.db.models
import django.http
import django.shortcuts

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


__all__ = ['item_detail', 'item_list', 'get_int', 'converter']
