from django.contrib import admin
from .models import Utilisateur, ModeDeTransport, Voyage, Reservation, Herbergement
# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(ModeDeTransport)
admin.site.register(Voyage)
admin.site.register(Reservation)
admin.site.register(Herbergement)
