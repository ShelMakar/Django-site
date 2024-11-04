import django.urls

import homepage.views

app_name = 'homepage'

urlpatterns = [
    django.urls.path('coffee/', homepage.views.coffee, name='coffee'),
    django.urls.path('echo/', homepage.views.echo, name='echo'),
    django.urls.path(
        'echo/submit/',
        homepage.views.echo_submit,
        name='echo_submit',
    ),
    django.urls.path('', homepage.views.home, name='home'),
]
