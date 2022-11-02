
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.reset, name='reset'),
    path('about/', views.about, name='about'),
    path('configuration/', views.configuration, name='configuration'),
    path('consumption/', views.consumption, name='consumption'),
    path('operations/', views.operation, name='operations'),
    path('consult/', views.consult, name='consult'),
    path('create/', views.create, name='create'),
    path('bill/', views.bill, name='bill'),
    path('report/', views.report, name='report'),
    path('create/resource/', views.create_resource, name='create_resource'),
    path('create/client/', views.create_client, name='create_client'),
    path('create/instance/', views.create_instance, name='create_instance'),
    path('create/bill/', views.create_bill, name='create_bill'),
    

]