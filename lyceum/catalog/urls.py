import catalog.converter
import catalog.views

from django.urls import path, re_path
from django.urls import register_converter


register_converter(catalog.converter.OnlyPolozhInt, 'polozh_int')

urlpatterns = [
    path('', catalog.views.item_list),
    path('<int:el>/', catalog.views.item_detail),
    re_path(r're/(?P<page_number>0*[1-9][0-9]*)/$', catalog.views.get_int),
    path('converter/<polozh_int:el>/', catalog.views.converter),
]
