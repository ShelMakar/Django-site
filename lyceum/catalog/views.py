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
        catalog.models.Item.objects.published(), pk=pk,
    )
    context = {'item': item}
    return django.shortcuts.render(request, template, context)


# def item_list(request):
#     template = 'catalog/item_list.html'
#     context = {
#         'out': [
#             {
#                 'id': 1,
#                 'name': 'Куриная шаурма',
#                 'text': 'Блаженство, включающее в себя мясо курицы.',
#                 'img': 'chiken_shav.jpg',
#             },
#             {
#                 'id': 2,
#                 'name': 'Хачапури по-аджарски',
#                 'text': 'Родом из Грузии.',
#                 'img': 'Danila.jpg',
#             },
#             {
#                 'id': 3,
#                 'name': 'Шашлык из барашка',
#                 'text': 'Нежнейшее мясо.',
#                 'img': 'shashlyck_baran.jpg',
#             },
#         ],
#     }
#     return django.shortcuts.render(request, template, context)


# def item(request, el):
#     template = 'catalog/item.html'
#     out = [
#         {
#             'id': 1,
#             'name': 'Куриная шаурма',
#             'text': 'Блаженство, включающее в себя мясо курицы.',
#             'img': 'chiken_shav.jpg',
#         },
#         {
#             'id': 2,
#             'name': 'Хачапури по-аджарски',
#             'text': 'Шедевр грузинских поваров. '
#             'Сыр, яйико, хрустящее тесто. Что еще нужно для счастья?',
#             'img': 'Danila.jpg',
#         },
#         {
#             'id': 3,
#             'name': 'Шашлык из барашка',
#             'text': 'Сочный, мощный шашлык из молодого барашка, '
#             'бережно замаринованный и пожаренный прямо на огне!',
#             'img': 'shashlyck_baran.jpg',
#         },
#     ]
#     not_found = {
#         'id': None,
#         'name': 'Товар не найден',
#         'text': '',
#         'img': '',
#     }
#     if el <= len(out):
#         return django.shortcuts.render(request, template, out[el - 1])
#     return django.shortcuts.render(request, template, not_found)


__all__ = ['item_detail', 'item_list', 'get_int', 'converter']
