from django.urls import path, re_path
from django.urls import register_converter

from . import converter, views


register_converter(converter.OnlyPolozhInt, 'polozh_int')

urlpatterns = [
    path('', views.item_list),
    path('<int:el>/', views.item_detail),
    re_path(r're/(?P<page_number>0*[1-9][0-9]*)/$', views.get_int),
    path('converter/<polozh_int:el>/', views.converter),
]
