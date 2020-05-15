from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField

class Item(models.Model):
    titre = models.CharField(max_length=100)
    prix = models.FloatField()
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.titre

class Individu(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    mail = models.EmailField(max_length=80)
    adresse = models.CharField(max_length=150)
    num = models.IntegerField(default=0)
    ville = models.CharField(max_length=50)
    code_postal = models.IntegerField()
    pays = models.CharField(max_length=50)
    nombre_de_commandes = models.IntegerField(default=0)
    somme_totale_depensee = models.FloatField(default=0)
    commentaires = models.CharField(max_length=300, default=None,blank=True, null=True)
    categorie_soc = models.CharField(max_length=50)
    caracteristique_comm = models.CharField(max_length=50)
    date = models.DateTimeField('Date naissance', default=None)
    nom_complet = models.CharField(max_length=100)
    date_passage_client = models.DateTimeField('Date creation client', default="",null=True, blank=True)

    def __str__(self):
        return self.prenom + " " + self.nom

class DernieresPublicites(models.Model):
    titre = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True)
    pub_date = models.DateTimeField('Date de publication', default=None)

class Envoi(models.Model):
    date_pub = models.DateTimeField('Date', default=None)

class Mail(models.Model):
    contenu = RichTextField(verbose_name="")


class Anomalie(models.Model):
    num_commande = models.CharField(max_length=50)
    individu =  models.ForeignKey(Individu, on_delete=models.CASCADE, related_name='individu_commande', null=True, default=None) 
    statut = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date de publication', default=None)


class CibleRoutage(models.Model):
    categorie_socio_professionelle = models.CharField(max_length=50)
    age_minimum = models.IntegerField()
    age_maximum = models.IntegerField()       
    departement = models.CharField(max_length=50)
    individus_selectionnes = models.CharField(max_length=100)
    type_canal = models.CharField(max_length=10)
    type_papier = models.CharField(max_length=15, default=None,blank=True, null=True)
    titre = models.CharField(max_length=50)           
    description = models.CharField(max_length=300)
    articles_selec = models.CharField(max_length=300)
    statut = models.BooleanField(default = False)

    def __str__(self):
        return self.titre + " - " + self.type_canal

class ItemCommande(models.Model):
    item_existant = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='article', default=None)
    quantite = models.IntegerField(default=0)

class Commande(models.Model):
    individu = models.ForeignKey(Individu, on_delete=models.CASCADE ) 
    type_reglement = models.CharField(max_length=20)
    montant = models.IntegerField()
    articles = models.ManyToManyField(ItemCommande)
    valide = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Date de création', default=None)

    class Meta:
        abstract = True

class CommandeCheque(Commande):
    num_cheque = models.IntegerField()
    nom_banque = models.CharField(max_length=100)
    signe = models.BooleanField(default=True)


class CommandeCarteBancaire(Commande):
    num_carte = models.IntegerField()
    date_expiration = models.DateTimeField('Date d\'expiration', default=None)
    carte_valide = models.BooleanField(default=True)

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="Avatar/", blank=True, null=True)