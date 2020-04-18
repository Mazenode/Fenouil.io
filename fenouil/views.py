from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from fenouil.models import Item, Client, Envoi, Anomalie
from fenouil.forms import MailForm
import boto3
import smtplib
from email.message import EmailMessage

clients = Client.objects.all()
items = Item.objects.all()
anomalies = Anomalie.objects.all()

def accueil(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/dashboard.html')

def articles(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/articles.html', {'items': items})

def client(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/client.html', {'clients': clients})

def envoi_mail(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':
            form = MailForm(request.POST)
            if form.is_valid():

                #On vérifie que l'utilisateur à entré au moins un mail
                if request.POST.get('mail2') == "Ou choisir le mail d'un de vos clients":
                    if request.POST.get('mail') == "":
                        messages.info(request, 'Vous devez entrer au moins un numéro de téléphone !')
                        return redirect('envoi_mail_form')
                    else :
                        addr = request.POST.get('mail')

                #On vérifie que l'utilisateur n'a pas entré plus d'un mail
                elif request.POST.get('mail2') != "Ou choisir le mail d'un de vos clients" and request.POST.get('mail') != "":
                    messages.info(request, 'Vous avez entrer deux mail différents !')
                    return redirect('envoi_mail_form')

                #Sinon, on valide.
                else:
                    addr = request.POST.get('mail2')
                
                #On vérifie qu'un numéro à été rentré
                if request.POST.get('num') == "Numéro de la publicité":
                    messages.info(request, 'Le numéro de la publicité n\'a pas été rentrée !')
                    return redirect('envoi_mail_form')
                else :
                    num = request.POST.get('num')

                sujet = request.POST.get('sujet')
                
                mail = form.save(commit=False)
               
                msg = EmailMessage()
                msg['Subject'] = sujet
                msg['From'] = 'serviceclient.decoperso@gmail.com'
                msg['To'] = addr
                msg.set_content(' ')
                msg.add_alternative(mail.contenu, subtype='html')

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login('serviceclient.decoperso@gmail.com','nxtlpmwvcpxpdhhn')

                    smtp.send_message(msg)

        
                return render(request, 'fenouil/envoi_mail_form.html', {'form' : form})

        else :
            form = MailForm()

        return render(request, 'fenouil/envoi_mail_form.html', {'form' : form})

def envoi_SMS(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            #On vérifie que l'utilisateur à entré au moins un numéro
            if request.POST.get('num_tel2') == "Ou choisir le numéro de téléphone d'un de vos clients":
                if request.POST.get('num_tel') == "":
                    messages.info(request, 'Vous devez entrer au moins un numéro de téléphone !')
                    return redirect('envoi_SMS')
                else :
                    num_tel = request.POST.get('num_tel')

            #On vérifie que l'utilisateur n'a pas entré plus d'un numéro
            elif request.POST.get('num_tel2') != "Ou choisir le numéro de téléphone d'un de vos clients" and request.POST.get('num_tel') != "":
                messages.info(request, 'Vous avez entrer deux numéros différents !')
                return redirect('envoi_SMS')

            #Sinon, on valide.
            else:
                num_tel = request.POST.get('num_tel2')
            
            #On vérifie qu'un numéro à été rentré
            if request.POST.get('num') == "Numéro de la publicité":
                messages.info(request, 'Le numéro de la publicité n\'a pas été rentrée !')
                return redirect('envoi_SMS')
            else :
                num = request.POST.get('num')

            texte = request.POST.get('texte')

            #envoi = Envoi(date = date, num = num)
            #envoi.save()
            
            #Permet l'envoi de messages
            client = boto3.client('sns', 'eu-west-1')
            client.publish(PhoneNumber = num_tel, Message = texte)
            
            return render(request, 'fenouil/envoi_SMS.html')

        else :
            return render(request, 'fenouil/envoi_SMS.html')

def envoi_papier(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':
            #On vérifie que la date est valide
            if request.POST.get('date') == "":
                messages.info(request, 'La date n\'a pas été rentrée !')
                return redirect('envoi_papier')
            else :
                date = request.POST.get('date')

            #On vérifie que l'utilisateur à entré au moins une adresse
            if request.POST.get('adresse2') == "Ou choisir une adresse d'un de vos clients":
                if request.POST.get('adresse') == "":
                    messages.info(request, 'Vous devez entrer au moins une adresse !')
                    return redirect('envoi_papier')
                else :
                    adresse = request.POST.get('adresse')

            #On vérifie que l'utilisateur n'a pas entré plus d'une adresse
            elif request.POST.get('adresse2') != "Ou choisir une adresse d'un de vos clients" and request.POST.get('adresse') != "":
                messages.info(request, 'Vous avez entrer deux adresses différentes !')
                return redirect('envoi_papier')

            #Sinon, on valide.
            else:
                adresse = request.POST.get('adresse2')
            
            #On vérifie qu'un numéro à été rentré
            if request.POST.get('num') == "Numéro de la publicité":
                messages.info(request, 'Le numéro de la publicité n\'a pas été rentrée !')
                return redirect('envoi_papier')
            else :
                num = request.POST.get('num')
            
            envoi = Envoi(date = date, num = num)
            envoi.save()

            return render(request, 'fenouil/envoi_papier.html')

        else :
            return render(request, 'fenouil/envoi_papier.html')

def creer_client(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            client = Client(
                prenom = request.POST.get('prenom'), 
                nom = request.POST.get('nom'), 
                adresse = request.POST.get('adresse'),
                mail = request.POST.get('mail'),
                num = request.POST.get('num_tel'),
                ville = request.POST.get('ville'),
                pays = request.POST.get('pays'),
                code_postal = request.POST.get('code_postal'),
                nombre_de_commandes = request.POST.get('nombre_commandes'),
                somme_totale_depensee = request.POST.get('somme_totale'),
                commentaires = request.POST.get('commentaires'),
                )

            client.save()

            return render(request, 'fenouil/creer_client.html')

        else :
            return render(request, 'fenouil/creer_client.html')

def liste_anomalies(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/liste_anomalies.html', {'anomalies': anomalies})

def signaler_anomalie(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            anomalie = Anomalie(
                num_commande = request.POST.get('num'), 
                statut = request.POST.get('statut'), 
                description = request.POST.get('texte'),
                pub_date = timezone.now()
                )

            anomalie.save()

            return render(request, 'fenouil/signaler_anomalie.html')

        else :
            return render(request, 'fenouil/signaler_anomalie.html')
