from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

def reset(request):
    send_mail(
        'Demande de nouveau mot de passe',
        'Bonjour Quentin, Réinitialisons votre mot de passe afin que vous puissiez continuer à utiliser notre application.',
        'admin@webee.com',
        ['to@example.com'],
        fail_silently=False,
    )

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("ok")
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Le nom d'utilisateur ou le mot de passe est incorrect.")
            return redirect('login')

    else:
        return render(request, "fenouil/log_form.html")

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            # On test si la charte à bien été acceptée
            if 'check' in request.POST:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Email déjà pris !")
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        password=password2,
                    )
                    user.save();
                    return redirect('/')
            else:
                messages.info(request, 'La charte n\' a pas été acceptée !')
                return redirect('register')

        else:
            messages.info(request, 'Les mots de passe ne correspondent pas !')
            return redirect('register')

    else:
        return render(request, "fenouil/reg_form.html")

def charte(request):
    return HttpResponse("Vous êtes sur la charte.")