import django.urls

import lyceum.settings

urlpatterns = [
    django.urls.path('', django.urls.include('homepage.urls')),
    django.urls.path('catalog/', django.urls.include('catalog.urls')),
    django.urls.path('about/', django.urls.include('about.urls')),
]

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (django.urls.path('__debug__/', django.urls.include(debug_toolbar.urls)),)
