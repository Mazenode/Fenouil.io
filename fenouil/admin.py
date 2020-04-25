from django.contrib import admin
from .models import Item, Individu, Mail, Anomalie, CibleRoutage

admin.site.register(Item)
admin.site.register(Individu)
admin.site.register(Mail)
admin.site.register(Anomalie)
admin.site.register(CibleRoutage)