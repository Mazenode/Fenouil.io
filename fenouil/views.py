from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from fenouil.models import Item, Individu, Envoi, Anomalie, CibleRoutage
from fenouil.forms import MailForm
import boto3
import smtplib
from email.message import EmailMessage

from django.core import serializers

individus = Individu.objects.all()
items = Item.objects.all()
anomalies = Anomalie.objects.all()
cibles = CibleRoutage.objects.all()

def accueil(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:

        nombre_anomalies_anciennes = 0
        nombre_anomalies_recentes = 0

        for anomalie in anomalies:
            if (anomalie.pub_date.month != timezone.now().month):
                nombre_anomalies_anciennes += 1

            else:
                nombre_anomalies_recentes += 1
        
        pourcentage_anomalies = ((nombre_anomalies_recentes - nombre_anomalies_anciennes)/ nombre_anomalies_anciennes) * 100

        if (nombre_anomalies_anciennes != 0):
            return render(request, 'fenouil/dashboard.html',
                { 'nombre_anomalies': nombre_anomalies_recentes, 'ratio_anomalies': round(pourcentage_anomalies, 2) }
                )
        else:
            return render(request, '404.html')

def articles(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/articles.html', {'items': items})

def individu(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/individu.html', {'individus': individus})

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
            individu = boto3.client('sns', 'eu-west-1')
            individu.publish(PhoneNumber = num_tel, Message = texte)
            
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

def creer_individu(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            individu = Individu(
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
                categorie_soc = request.POST.get('csp'),
                caracteristique_comm = request.POST.get('car_com'),
                date = request.POST.get('date_naissance'),
                )

            individu.save()

            return render(request, 'fenouil/creer_individu.html')

        else :
            return render(request, 'fenouil/creer_individu.html')

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

def creer_cible_routage(request, etape):

    global csp, age_min, age_max, departement, individus_selec

    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        
        if (etape == 1):
            if request.method == 'POST':
                
                csp = request.POST.get('csp'),
                age_min = request.POST.get('age_min')
                age_max = request.POST.get('age_max')           
                departement = request.POST.get('departement')
                individus_selec = request.POST.getlist('individus_selec')

                return HttpResponseRedirect('../../creer_cible_routage/2/')

            else :
                return render(request, 'fenouil/creer_cible_routage_1.html', {'individus': individus})
        elif (etape == 2):
            if request.method == 'POST':

                type_canal = request.POST.get('type')
                type_papier = request.POST.get('type_papier')
                titre = request.POST.get('titre')        
                description = request.POST.get('description')
                articles_selec = request.POST.getlist('articles_selec')

                cible = CibleRoutage(
                    categorie_socio_professionelle = csp,
                    age_minimum = age_min,
                    age_maximum = age_max,      
                    departement = departement,
                    individus_selectionnes = str(individus_selec),
                    type_canal = type_canal,
                    type_papier = type_papier,
                    titre = titre,         
                    description = description,
                    articles_selec = str(articles_selec)
                    )

                cible.save()

                #On serialize la derniere cible de routage (celle que l'on vient de créer) en xml
                #queryset = serializers.serialize('xml', CibleRoutage.objects.filter(pk=CibleRoutage.objects.count()-1))
                
                #return HttpResponse(queryset, content_type="application/xml")

                return render(request, 'fenouil/creer_cible_routage_1.html', {'individus': individus})

            else :
                return render(request, 'fenouil/creer_cible_routage_2.html', {'items': items})
        else:
            return render(request, '404.html')

def valider_cible_routage(request):
    if not request.user.is_authenticated:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            cible = CibleRoutage.objects.get(pk=request.POST.get('pk'))

            print('Avant = ',cible.statut)
            cible.statut = True
            cible.save()

            print('Après = ', cible.statut)

            return render(request, 'fenouil/valider_cible_routage.html', {'cibles': cibles})

        else:
            return render(request, 'fenouil/valider_cible_routage.html', {'cibles': cibles})