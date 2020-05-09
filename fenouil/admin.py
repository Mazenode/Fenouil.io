from django.contrib import admin
from .models import Item, Individu, Mail, Anomalie, CibleRoutage, CommandeCheque, CommandeCarteBancaire, ItemCommande, Envoi, UserProfile
admin.site.register(Item)
admin.site.register(Individu)
admin.site.register(Mail)
admin.site.register(Anomalie)
admin.site.register(CibleRoutage)
admin.site.register(CommandeCheque)
admin.site.register(CommandeCarteBancaire)
admin.site.register(ItemCommande)
admin.site.register(Envoi)
admin.site.register(UserProfile)