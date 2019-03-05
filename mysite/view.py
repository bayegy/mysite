
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def get_html(request):
    context = {}
    context['var1'] = 'Hello World QWQ!'
    return render(request, 'main.html', context)
