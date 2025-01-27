import django.urls

import catalog.converters
import catalog.views

app_name = "catalog"

django.urls.register_converter(
    catalog.converters.ConverterNumbersCatalog,
    "number",
)

urlpatterns = [
    django.urls.path(
        "",
        catalog.views.ItemListView.as_view(),
        name="item_list",
    ),
    django.urls.path(
        "<int:converter>/",
        catalog.views.ItemDetailView.as_view(),
        name="item_detail",
    ),
    django.urls.path(
        "converter/<number:num>/",
        catalog.views.ConverterView.as_view(),
        name="converter",
    ),
    django.urls.path(
        "new/",
        catalog.views.NewItemsView.as_view(),
        name="new_items",
    ),
    django.urls.path(
        "friday/",
        catalog.views.FridayItemsView.as_view(),
        name="friday_items",
    ),
    django.urls.path(
        "unverified/",
        catalog.views.UnverifiedItemsView.as_view(),
        name="unverified",
    ),
    django.urls.re_path(
        r"re/(?P<p>\d+)/",
        catalog.views.RegularView.as_view(),
        name="regular",
    ),
]
