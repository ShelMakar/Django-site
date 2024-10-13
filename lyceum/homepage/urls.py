import django.urls

import homepage.views

urlpatterns = [
    django.urls.path('coffee/', homepage.views.tea),
    django.urls.path('', homepage.views.home),
]
