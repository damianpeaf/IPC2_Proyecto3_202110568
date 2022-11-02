
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.reset, name='reset'),
    path('about/', views.about, name='about'),
    path('configuration/', views.configuration, name='configuration'),
    path('consumption/', views.consumption, name='consumption'),
    path('operations/', views.operation, name='operations')
]