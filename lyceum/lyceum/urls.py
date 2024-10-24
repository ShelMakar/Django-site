import django.contrib.admin
import django.urls

import lyceum.settings

urlpatterns = [
    django.urls.path('', django.urls.include('homepage.urls')),
    django.urls.path('catalog/', django.urls.include('catalog.urls')),
    django.urls.path('about/', django.urls.include('about.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path(
        'ckeditor5/', django.urls.include('django_ckeditor_5.urls'),
    ),
] + django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            '__debug__/',
            django.urls.include(debug_toolbar.urls),
        ),
    )
