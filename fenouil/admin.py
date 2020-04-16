from django.contrib import admin
from .models import Item, Client, Mail

admin.site.register(Item)
admin.site.register(Client)
admin.site.register(Mail)