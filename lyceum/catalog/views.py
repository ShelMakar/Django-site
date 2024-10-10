import django.http


def item_list(request):
    return django.http.HttpResponse('<body>Список элементов</body>')


def item_detail(request, el):
    return django.http.HttpResponse('<body>Подробно элемент</body>')


def get_int(request, page_number):
    return django.http.HttpResponse(page_number)


def converter(request, el):
    return django.http.HttpResponse(el)
