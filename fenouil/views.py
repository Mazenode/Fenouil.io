from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse


def accueil(request):
    return render(request, 'fenouil/index.html')


