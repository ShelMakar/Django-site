import django.conf
import django.conf.urls.static
import django.contrib.admin
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

admin_and_editor_urls = [
    django.urls.path('admin/', django.contrib.admin.site.urls, name='admin'),
    django.urls.path(
        'ckeditor5/',
        django.urls.include('django_ckeditor_5.urls'),
    ),
]

urlpatterns = app_urls + admin_and_editor_urls

if lyceum.settings.DEBUG:
    urlpatterns += static_urls

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        django.urls.path(
            '__debug__/',
            django.urls.include(debug_toolbar.urls),
        ),
    ]
