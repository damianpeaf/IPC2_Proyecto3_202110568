from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def reset(request):
    return render(request, 'reset.html')

def configuration(request):
    return render(request, 'configuration.html')

def consumption(request):
    return render(request, 'consumption.html')

def about(request):
    return render(request, 'about.html')

def operation(request):
    return render(request, 'operations.html')