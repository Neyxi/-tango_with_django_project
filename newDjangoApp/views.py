from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("newDjangoApp says hey there partner!")

def restricted(request):
    return HttpResponse('This is a restricted page. You must be logged in to see it.')


