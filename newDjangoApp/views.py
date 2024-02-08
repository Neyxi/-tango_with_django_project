from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("newDjangoApp says hey there partner!")


