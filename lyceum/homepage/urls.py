from django.urls import path

from . import views

urlpatterns = [
    path('coffee/', views.tea),
    path('', views.home),
]
