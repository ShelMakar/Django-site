import django.urls
import django.contrib

import lyceum.settings

urlpatterns = [
    django.urls.path('', django.urls.include('homepage.urls')),
    django.urls.path('catalog/', django.urls.include('catalog.urls')),
    django.urls.path('about/', django.urls.include('about.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
]

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            '__debug__/', django.urls.include(debug_toolbar.urls)
        ),
    )
