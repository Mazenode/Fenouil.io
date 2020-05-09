from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from fenouil.models import Item, Individu, Anomalie, CibleRoutage, ItemCommande, Commande, CommandeCheque, CommandeCarteBancaire, Envoi, UserProfile
from fenouil.forms import MailForm
import boto3
import smtplib
from email.message import EmailMessage
import xml.etree.cElementTree as xml
import xml.dom.minidom as test
import json


from django.core import serializers

individus = Individu.objects.all()
items = Item.objects.all()
anomalies = Anomalie.objects.all()
cibles = CibleRoutage.objects.all()
commandes_cheque = CommandeCheque.objects.all()
commandes_carte = CommandeCarteBancaire.objects.all()
envois = Envoi.objects.all()

#Classe instanciée uniquement pour l'affichage des articles dans dashboard
class Article:
  def __init__(self, nom, ventes, benef):
    self.nom = nom
    self.ventes = ventes
    self.benef = benef


def accueil(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:

        #On calcul les différents pourcentages à afficher sur le dashboard

        #Calcul du pourcentage d'anomalies'
        nombre_anomalies_anciennes = 0
        nombre_anomalies_recentes = 0

        for anomalie in anomalies:
            if (anomalie.pub_date.month != timezone.now().month):
                nombre_anomalies_anciennes += 1

            else:
                nombre_anomalies_recentes += 1

        if (nombre_anomalies_recentes == 0 or nombre_anomalies_anciennes == 0):
            pourcentage_anomalies = 0
        else :
            pourcentage_anomalies =  getPourcentage(nombre_anomalies_recentes, nombre_anomalies_anciennes)

        #Calcul du pourcentage de nouveaux clients
        nombre_clients_anciens = 0
        nombre_clients_recents = 0

        for individu in individus:
            if (individu.caracteristique_comm == 'client'):
                if (individu.date_passage_client.month != timezone.now().month):
                    nombre_clients_anciens += 1

                else:
                    nombre_clients_recents += 1

        if (nombre_clients_recents == 0 or nombre_clients_anciens == 0):
            pourcentage_clients = 0
        else :
            pourcentage_clients =  getPourcentage(nombre_clients_recents, nombre_clients_anciens)
        

        #Calcul du pourcentage de commandes
        nombre_commandes_anciennes = 0
        nombre_commandes_recentes = 0

        for commande in commandes_cheque:
            if (commande.pub_date.month != timezone.now().month):
                nombre_commandes_anciennes += 1

            else:
                nombre_commandes_recentes += 1

        for commande in commandes_carte:
            if (commande.pub_date.month != timezone.now().month):
                nombre_commandes_anciennes += 1

            else:
                nombre_commandes_recentes += 1

        if (nombre_commandes_recentes == 0 or nombre_commandes_anciennes == 0):
            pourcentage_commandes = 0
        else :
            pourcentage_commandes =  getPourcentage(nombre_commandes_recentes, nombre_commandes_anciennes)


        #Graphe des ventes
        tous_les_mois = ['jan', 'fev', 'mars', 'avr', 'mai', 'juin', 'juil', 'août', 'sep', 'oct', 'nov', 'dec']
        liste_benef = []


        index = timezone.now().month-1
        liste_mois = []

        for i in range(8):
            if(index - 1 == -1):
                index = 12
            liste_mois.append(tous_les_mois[index-i])

        liste_mois.reverse()

        liste_benef = []
        liste_benef_carte = []
        liste_benef_cheque = []

        for mois in liste_mois:
            total = 0

            for commande in CommandeCheque.objects.all():
                
                if (commande.pub_date.month == liste_mois.index(mois)):
                    total+=commande.montant
                    
            liste_benef_cheque.append(total)

            for commande in CommandeCarteBancaire.objects.all():
                
                if (commande.pub_date.month == liste_mois.index(mois)):
                    total+=commande.montant
                    
            liste_benef_carte.append(total)

        liste_benef = [x + y for x, y in zip(liste_benef_cheque, liste_benef_carte)]

        valeur = liste_benef[6:8]
        liste_benef.insert(0, valeur[0])
        liste_benef.insert(1, valeur[1])

        json_mois = json.dumps(liste_mois)
        json_benef = json.dumps(liste_benef)

        #Graphes des publicités envoyées

        liste_6_mois = liste_mois[2:8]

        json_6_mois = json.dumps(liste_6_mois)

        liste_nb_pubs = []

        for i in range(6):
            total = 0
            for envoi in envois:
                if (envoi.date_envoi.month == timezone.now().month - i):
                    total +=1
            liste_nb_pubs.append(total)

        liste_nb_pubs.reverse()

        json_nb_pubs = json.dumps(liste_nb_pubs)

        return render(request, 'fenouil/dashboard.html',
            { 
                'nombre_anomalies': nombre_anomalies_recentes, 
                'ratio_anomalies': round(pourcentage_anomalies, 2),
                'nombre_clients': nombre_clients_recents, 
                'ratio_clients': round(pourcentage_clients, 2),
                'nombre_commandes': nombre_commandes_recentes, 
                'ratio_commandes': round(pourcentage_commandes, 2),
                'liste_mois':json_mois,
                'liste_benef':json_benef,
                'liste_6_mois':json_6_mois,
                'liste_nb_pubs':json_nb_pubs,
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),
                'articles':getArticlesLesPlusVendus(),
            })


def getPourcentage(recent, ancien):
    return ((recent - ancien)/ ancien) * 100

def articles(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/articles.html', {
            'items': items,
            'liste_permissions':getPermissionsUser(request),
            'liste_identifiants_user':getNomUser(request),
            'photo_user':getPhotoUser(request)
            })

def individu(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        return render(request, 'fenouil/individu.html', {
            'individus': individus,
            'liste_permissions':getPermissionsUser(request),
            'liste_identifiants_user':getNomUser(request),
            'photo_user':getPhotoUser(request),
            })

def envoi_mail(request):
    if not request.user.is_staff:
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

                envoi = Envoi(
                    date_envoi = timezone.now()
                    )
                envoi.save()
        
                return render(request, 'fenouil/envoi_mail_form.html',{
                    'form' : form,
                    'liste_permissions':getPermissionsUser(request),
                    'liste_identifiants_user':getNomUser(request),
                    'photo_user':getPhotoUser(request),
                    })

        else :
            form = MailForm()

        return render(request, 'fenouil/envoi_mail_form.html', {
            'form' : form,
            'liste_permissions':getPermissionsUser(request),
            'liste_identifiants_user':getNomUser(request),
            'photo_user':getPhotoUser(request),
            })

def envoi_SMS(request):
    if not request.user.is_staff:
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

            envoi = Envoi(
                    date_envoi = timezone.now()
                    )
            envoi.save()
            
            
            return render(request, 'fenouil/envoi_SMS.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),
                })

        else :
            return render(request, 'fenouil/envoi_SMS.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

def envoi_papier(request):
    if not request.user.is_staff:
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

            envoi = Envoi(
                    date_envoi = timezone.now()
                    )
            envoi.save()
        

            return render(request, 'fenouil/envoi_papier.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

        else :
            return render(request, 'fenouil/envoi_papier.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),
                })

def creer_individu(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            if (request.POST.get('nombre_commandes')=='') :
                nombre_commandes = 0
            else :
                nombre_commandes = request.POST.get('nombre_commandes')
                date_passage_client = timezone.now()

            if (request.POST.get('somme_totale')=='') :
                somme_totale = 0.0
            else :
                somme_totale = request.POST.get('somme_totale')

            if (request.POST.get('car_com') == 'client'):
                date_passage_client = timezone.now()
            else:
                date_passage_client = None

            individu = Individu(
                prenom = request.POST.get('prenom'), 
                nom = request.POST.get('nom'), 
                adresse = request.POST.get('adresse'),
                mail = request.POST.get('mail'),
                num = request.POST.get('num_tel'),
                ville = request.POST.get('ville'),
                pays = request.POST.get('pays'),
                code_postal = request.POST.get('code_postal'),
                nombre_de_commandes = nombre_commandes,
                somme_totale_depensee = request.POST.get('somme_totale'),
                commentaires = somme_totale,
                categorie_soc = request.POST.get('csp'),
                caracteristique_comm = request.POST.get('car_com'),
                date = request.POST.get('date_naissance'),
                nom_complet = request.POST.get('prenom') + " " +request.POST.get('nom'),  
                date_passage_client = date_passage_client
                )

            individu.save()

            return HttpResponseRedirect('../creer_individu')

        else :
            return render(request, 'fenouil/creer_individu.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),
                })

def liste_anomalies(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            num_commande = request.POST.get('anomalie_id')
            s = []
            n = []

            for lettre in num_commande:
                if lettre.isalpha():
                    s.append(lettre)
                elif lettre.isdigit():
                    n.append(lettre)

            s = ''.join(s)
            n = ''.join(n)
            
            if s == 'cheque':
                commande = CommandeCheque.objects.filter(pk= n).update(valide='valide')
                Anomalie.objects.filter(num_commande=num_commande).delete()
                commande.individu.update(caracteristique_comm='client')
            elif s == 'carte':
                CommandeCarteBancaire.objects.filter(pk= n).update(valide='valide')
                Anomalie.objects.filter(num_commande=num_commande).delete()


            return render(request, 'fenouil/liste_anomalies.html', {
                'anomalies': anomalies,
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

        else :
            return render(request, 'fenouil/liste_anomalies.html', {
                'anomalies': anomalies,
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})
        
def signaler_anomalie(request):
    if not request.user.is_staff:
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

            return render(request, 'fenouil/signaler_anomalie.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

        else :
            return render(request, 'fenouil/signaler_anomalie.html',{
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

def creer_cible_routage(request, etape):

    global csp, age_min, age_max, departement, individus_selec

    if not request.user.is_staff:
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
                return render(request, 'fenouil/creer_cible_routage_1.html', {
                    'individus': individus,
                    'liste_permissions':getPermissionsUser(request),
                    'liste_identifiants_user':getNomUser(request),
                    'photo_user':getPhotoUser(request),})
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

                root=xml.Element("CibleRoutage")
                support=xml.SubElement(root, "support")
                support.text = type_canal

                liste_individus=xml.SubElement(root, "liste_individus")
                for individu in individus_selec:
                    try:
                        nouvel_individu = Individu.objects.get(nom_complet = individu)
                    except SomeModel.DoesNotExist:
                        go = None
                    
                    individu_xml=xml.SubElement(liste_individus, "individu")

                    mail_xml= xml.SubElement(individu_xml, "mail")
                    mail_xml.text = nouvel_individu.mail

                    numero= xml.SubElement(individu_xml, "numero")
                    numero.text = str(nouvel_individu.num)

                    ville= xml.SubElement(individu_xml, "ville")
                    ville.text = nouvel_individu.ville


                nom=xml.SubElement(root, "Nom")
                nom.text = titre

                description_xml=xml.SubElement(root, "description")
                description_xml.text = description
                tree = xml.ElementTree(root)

                liste_articles=xml.SubElement(root, "liste_articles")
                for article in articles_selec:
                    try:
                        nouvel_article = Item.objects.get(titre = article)
                    except SomeModel.DoesNotExist:
                        go = None
                    
                    article_xml=xml.SubElement(liste_articles, "articles")

                    titre_xml= xml.SubElement(article_xml, "nom")
                    titre_xml.text = nouvel_article.titre

                    prix_xml= xml.SubElement(article_xml, "prix")
                    prix_xml.text = str(nouvel_article.prix)


                xmlstr = test.parseString(xml.tostring(root)).toprettyxml(indent="   ")

                nom_fichier = "media/CibleRoutageXML/" + str(cible.pk) + ".xml"

                with open(nom_fichier, "w") as f:
                    f.write(xmlstr)
                

                return render(request, 'fenouil/creer_cible_routage_1.html', {
                    'individus': individus,
                    'liste_permissions':getPermissionsUser(request),
                    'liste_identifiants_user':getNomUser(request),
                    'photo_user':getPhotoUser(request),})

            else :
                return render(request, 'fenouil/creer_cible_routage_2.html', {
                    'items': items,
                    'liste_permissions':getPermissionsUser(request),
                    'liste_identifiants_user':getNomUser(request),
                    'photo_user':getPhotoUser(request),})
        else:
            return render(request, '404.html')

def valider_cible_routage(request):
    cibles_filtrees = CibleRoutage.objects.filter(statut=False)
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':
            if "valide" in request.POST:
                cible = CibleRoutage.objects.get(pk=request.POST.get('pk'))
                cible.statut = True
                cible.save()

                return render(request, 'fenouil/valider_cible_routage.html', {
                    'cibles': cibles_filtrees,
                    'liste_permissions':getPermissionsUser(request),
                    'liste_identifiants_user':getNomUser(request),
                    'photo_user':getPhotoUser(request),})

            elif "display" in request.POST:
                nom_redirection = "media/CibleRoutageXML/" + request.POST.get('pk') + ".xml"
                return HttpResponse(open(nom_redirection).read(), content_type="application/xml")

        else:
            return render(request, 'fenouil/valider_cible_routage.html', {
                'cibles': cibles_filtrees,
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

def saisir_commande(request):
    if not request.user.is_staff:
        return render(request, 'fenouil/accueil.html')
    else:
        if request.method == 'POST':

            individu = Individu.objects.get(nom_complet= request.POST.get('individu'))
            liste_articles = request.POST.getlist('liste_article')
            type_reglement = request.POST.get('type_reglement')
            montant = request.POST.get('montant_commande')
            num = request.POST.get('num')

            if (type_reglement == 'Chèque'):
                nom_banque = request.POST.get('nom-date_value')
                if(request.POST.get('etat-valide') == 'Signé'):
                    etat_cheque = True
                else :
                    etat_cheque = False

                commande_cheque = CommandeCheque(
                        individu=individu,
                        type_reglement=type_reglement,
                        montant=montant,
                        num_cheque=num,
                        nom_banque=nom_banque,
                        signe=etat_cheque,
                        pub_date=timezone.now()
                    )
                commande_cheque.save()

            elif (type_reglement == 'Carte bancaire'):
                date = request.POST.get('nom-date_value')
                if(request.POST.get('etat-valide') == 'Valide'):
                    etat_carte = True
                else :
                    etat_carte = False

                commande_carte = CommandeCarteBancaire(
                        individu=individu,
                        type_reglement=type_reglement,
                        montant=montant,
                        num_carte=num,
                        date_expiration=date,
                        carte_valide=etat_carte,
                        pub_date=timezone.now()
                    )
                commande_carte.save()


            liste = []
            compteur = request.POST.get('compteur')

            for i in range(1, int(compteur)+1):
                article = request.POST.get('item'+str(i))
                item_commande = ItemCommande(item_existant = Item.objects.get(titre=article), quantite = request.POST.get('quantite'+str(i)))
                item_commande.save()
                liste.append(item_commande)


            #On calcule le total
            total = 0
            for item in liste:
                total += item.item_existant.prix * float(item.quantite)

            

            if (type_reglement == 'Chèque'):
                commande_cheque.articles.add(*liste)

                #On change le statut de la commande en fonction des anomalies
                if (total != float(montant)):

                    CommandeCheque.objects.filter(pk = commande_cheque.pk).update(valide='En attente')
                    commande_cheque.refresh_from_db()
                    anomalie = Anomalie(
                            num_commande =  'cheque' + str(commande_cheque.pk),
                            statut = 'Erreur sur le montant',
                            pub_date = timezone.now(),
                            individu = individu
                            )
                    anomalie.save() 
                else :
                    CommandeCheque.objects.filter(pk = commande_cheque.pk).update(valide='valide')
                    commande_cheque.refresh_from_db()

                if (etat_cheque != True):
                    CommandeCheque.objects.filter(pk = commande_cheque.pk).update(valide='En attente')
                    commande_cheque.refresh_from_db()       
                    anomalie = Anomalie(
                            num_commande =  'cheque' + str(commande_cheque.pk),
                            statut = 'Problème sur le moyen de paiement',
                            pub_date = timezone.now(),
                            individu = individu
                            )
                    anomalie.save() 
                else :
                    CommandeCheque.objects.filter(pk = commande_cheque.pk).update(valide='valide')
                    commande_cheque.refresh_from_db()
            
                if (CommandeCheque.objects.get(pk = commande_cheque.pk).valide == 'valide'):
                    individu.caracteristique_comm='client'
                    individu.save()

            elif (type_reglement == 'Carte bancaire'):
                commande_carte.articles.add(*liste)

                #On change le statut de la commande en fonction des anomalies
                if (total != float(montant)):
                    CommandeCarteBancaire.objects.filter(pk = commande_carte.pk).update(valide='En attente')
                    commande_carte.refresh_from_db()
                    anomalie = Anomalie(
                            num_commande =  'carte' + str(commande_carte.pk),
                            statut = 'Erreur sur le montant',
                            pub_date = timezone.now(),
                            individu = individu
                            )
                    anomalie.save() 
                else :
                    CommandeCarteBancaire.objects.filter(pk = commande_carte.pk).update(valide='valide')
                    commande_carte.refresh_from_db()

                if (etat_carte != True):
                    CommandeCarteBancaire.objects.filter(pk = commande_carte.pk).update(valide='En attente')
                    commande_carte.refresh_from_db()       
                    anomalie = Anomalie(
                            num_commande =  'carte' + str(commande_carte.pk),
                            statut = 'Problème sur le moyen de paiement',
                            pub_date = timezone.now(),
                            individu = individu
                            )
                    anomalie.save() 
                else :
                    CommandeCarteBancaire.objects.filter(pk = commande_carte.pk).update(valide='valide')
                    commande_carte.refresh_from_db()
            
                if (CommandeCarteBancaire.objects.get(pk = commande_carte.pk).valide == 'valide'):
                    individu.caracteristique_comm='client'
                    individu.save()

            return HttpResponseRedirect('/saisir_commande')

        else:
            return render(request, 'fenouil/saisir_commande.html', {
                'individus': individus, 
                'items': items,
                'liste_permissions':getPermissionsUser(request),
                'liste_identifiants_user':getNomUser(request),
                'photo_user':getPhotoUser(request),})

def getPermissionsUser(request):
    liste_groupe_user = []
    for groupe in request.user.groups.all():
            liste_groupe_user.append(str(groupe))
    return liste_groupe_user

def getNomUser(request):
    liste_identifiants_user = []
    liste_identifiants_user.append(request.user.first_name)
    liste_identifiants_user.append(request.user.last_name)
    return liste_identifiants_user

def getPhotoUser(request):
    if UserProfile.objects.filter(user = request.user).exists():
        return 'media/'+ UserProfile.objects.filter(user = request.user)[0].avatar.name
    else:
        return 'media/Avatar/default'

def getArticlesLesPlusVendus():

    #On récupère les 10 articles les plus vendus

    listes_noms_items = []
    i=0
    for item in Item.objects.order_by('prix'):
        if i < 10:
            listes_noms_items.append(item)
        i+=1


    nombre_de_ventes = []
    for item in listes_noms_items:
        if not ItemCommande.objects.filter(item_existant = item):
            nombre_de_ventes.append(0)
        else:
            tot = 0
            for i in range(len(ItemCommande.objects.filter(item_existant = item))):
                tot += ItemCommande.objects.filter(item_existant = item)[i].quantite
            nombre_de_ventes.append(tot)

    benef = [None] * len(listes_noms_items)
    for i in range(len(listes_noms_items)):
        benef[i] = nombre_de_ventes[i]* listes_noms_items[i].prix

    liste_articles = []
    for i in range(len(listes_noms_items)):
        article = Article(
                nom = str(listes_noms_items[i]),
                ventes = str(nombre_de_ventes[i]),
                benef = str(benef[i])
            )
        liste_articles.append(article)

    return liste_articles
