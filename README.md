# Fenouil.io
Tuto pour développer ou tester le projet de GPI

## Installation de Django
Pour commencer vous devez vérifier si Python est bien installé sur votre pc avec :
```bash
python --version
```
si c'est le cas vous devez taper :
```bash
pip install Django
```
sinon installez le et refaite la dernière commande.

## Utilisation de l'archive
Téléchargez l'archive en .zip depuis github et dé-zipper le là où vous voulez l'utiliser.

Le meilleur IDE pour voir le code c'est PyCharm, il y a la version Pro qui est gratuite pendant 1 mois et
qui permet d'utiliser Django, sinon n'importe quel éditeur de texte fait l'affaire.

Ensuite on ouvre le dossier ou se trouve le fichier manage.py depuis la console : 
```bash
cd --Le chemin de votre archive--
```
puis on lance le serveur avec :
```bash
python manage.py runserver
```
Après ça il vous propose le lien : http://127.0.0.1:8000/, vous cliquez dessus et vous êtes sur le site.

Pour vous deplacez sur le site il faut modifier directement l'url, par exemple je veux aller sur la page login, je change
http://127.0.0.1:8000/ en http://127.0.0.1:8000/login.html.

## Utilisation de la base de données
Le meilleur outil pour visualiser une base de donnée postgreSQL c'est pgAdmin4. Il faut le telecharger et ajouter un nouveau serveur en rentrant les codes que je vous ai envoyés dans la conv Telegram.

## Liens utiles
- Pour apprendre le Django il y a un très bon tuto sur le site officiel : https://docs.djangoproject.com/fr/3.0/intro/tutorial01/ les 4 premières parties sont les plus intéressantes.

- Pour installer Python : https://www.youtube.com/watch?v=YYXdXT2l-Gg

- pgAdmin4 : https://www.pgadmin.org/download/

- PyCharm : https://www.jetbrains.com/fr-fr/pycharm/
