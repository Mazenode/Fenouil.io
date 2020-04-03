from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from fenouil.models import Item, Client


def accueil(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/index.html')
    else:
        return render(request, 'fenouil/dashboard.html')

def articles(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/index.html')
    else:
        items = Item.objects.all()
        return render(request, 'fenouil/articles.html', {'items': items})

def client(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/index.html')
    else:
        clients = Client.objects.all()
        return render(request, 'fenouil/client.html', {'clients': clients})

