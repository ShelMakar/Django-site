import django.conf
import django.conf.urls.static
import django.urls

import catalog.converter
import catalog.views


app_name = 'catalog'

django.urls.register_converter(catalog.converter.OnlyPolozhInt, 'polozh_int')

urlpatterns = [
    django.urls.path('', catalog.views.item_list, name='item_list'),
    django.urls.path(
        '<int:pk>/',
        catalog.views.item_detail,
        name='item_detail',
    ),
    django.urls.re_path(
        r're/(?P<page_number>0*[1-9][0-9]*)/$',
        catalog.views.get_int,
        name='get_int',
    ),
    django.urls.path('converter/<polozh_int:el>/', catalog.views.converter),
    django.urls.path(
        'unverified', catalog.views.unverified, name='unverified',
    ),
    django.urls.path('friday', catalog.views.friday, name='friday'),
    django.urls.path('new', catalog.views.new, name='new'),
]
