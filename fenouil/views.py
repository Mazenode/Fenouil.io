from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm

def accueil(request):
    return HttpResponse("Vous êtes sur la page d'accueil de fenouil.io")

def login(request):
    return HttpResponse("Vous êtes sur la page de connexion.")

def register(request):
        # if request.method == 'POST':
        #     form = UserCreationForm(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         return redirect('')
        # else:
        #     form = UserCreationForm()
        #
        #     args = {'form : form'}
        return render(request, 'fenouil/register.html')


