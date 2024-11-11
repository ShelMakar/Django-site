import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import lyceum.settings


app_urls = [
    django.urls.path('', django.urls.include('homepage.urls')),
    django.urls.path('catalog/', django.urls.include('catalog.urls')),
    django.urls.path('about/', django.urls.include('about.urls')),
    django.urls.path('feedback/', django.urls.include('feedback.urls')),
    django.urls.path('download/', django.urls.include('download.urls')),
]

static_urls = django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)

admin_urls = [
    django.urls.path('admin/', django.contrib.admin.site.urls, name='admin'),
    django.urls.path('auth/', django.urls.include('users.urls')),
    django.urls.path('auth/', django.urls.include(django.contrib.auth.urls)),
]
editor_urls = [
    django.urls.path(
        'ckeditor5/',
        django.urls.include('django_ckeditor_5.urls'),
    ),
]

urlpatterns = app_urls + admin_urls + editor_urls

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        django.urls.path(
            '__debug__/',
            django.urls.include(debug_toolbar.urls),
        ),
    ] + static_urls
