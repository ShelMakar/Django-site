import catalog.converter
import catalog.views

import django.urls


django.urls.register_converter(catalog.converter.OnlyPolozhInt, 'polozh_int')

urlpatterns = [
    django.urls.path('', catalog.views.item_list),
    django.urls.path('<int:el>/', catalog.views.item_detail),
    django.urls.re_path(
        r're/(?P<page_number>0*[1-9][0-9]*)/$', catalog.views.get_int
    ),
    django.urls.path('converter/<polozh_int:el>/', catalog.views.converter),
]
