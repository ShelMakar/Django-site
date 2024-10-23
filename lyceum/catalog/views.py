import django.http
import django.shortcuts


def item_detail(request, el):
    return django.http.HttpResponse('<body>Подробно элемент</body>')


def get_int(request, page_number):
    return django.http.HttpResponse(page_number)


def converter(request, el):
    return django.http.HttpResponse(el)


def item_list(request):
    template = 'catalog/item_list.html'
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


def item(request, el):
    template = 'catalog/item.html'
    out = [
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
    ]

    return django.shortcuts.render(request, template, out[el - 1])
