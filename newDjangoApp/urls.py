from django.urls import path
from newDjangoApp import views

app_name = 'newDjangoApp'

urlpatterns = [
    path('', views.index, name='index'),
]