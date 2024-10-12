import about.views

from django.urls import path


urlpatterns = [
    path('', about.views.description),
]
