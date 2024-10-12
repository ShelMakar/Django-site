from django.urls import path

import homepage.views

urlpatterns = [
    path('coffee/', homepage.views.tea),
    path('', homepage.views.home),
]
