from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField

class Item(models.Model):
    titre = models.CharField(max_length=100)
    prix = models.FloatField()
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.titre

class Client(models.Model):
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

    def __str__(self):
        return self.prenom + " " + self.nom

class Envoi(models.Model):
    date = models.CharField(max_length=8)
    num = models.CharField(max_length=100)

class Mail(models.Model):
    contenu = RichTextField(verbose_name="")

class Anomalie(models.Model):
    num_commande = models.CharField(max_length=50)
    statut = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date de publication', default=None)