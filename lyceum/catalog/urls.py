import django.conf
import django.conf.urls.static
import django.urls

import catalog.converter
import catalog.views
import lyceum.settings


app_name = 'catalog'

django.urls.register_converter(catalog.converter.OnlyPolozhInt, 'polozh_int')

urlpatterns = [
    django.urls.path('', catalog.views.item_list, name='item_list'),
    django.urls.path('<int:el>/', catalog.views.item, name='item'),
    django.urls.re_path(
        r're/(?P<page_number>0*[1-9][0-9]*)/$',
        catalog.views.get_int,
        name='get_int',
    ),
    django.urls.path('converter/<polozh_int:el>/', catalog.views.converter),
]
if lyceum.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
