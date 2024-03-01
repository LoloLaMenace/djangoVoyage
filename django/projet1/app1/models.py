from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=20, null=True)
    adresse = models.CharField(max_length=255, null=True)
    ville = models.CharField(max_length=255, null=True)
    mdp = models.CharField(max_length=255, null=True)


class ModeDeTransport(models.Model):
    idModeTransport = models.IntegerField(unique=True)
    mode = models.CharField(max_length=100)

class Voyage(models.Model):
    depart = models.CharField(max_length=255)
    arriver = models.CharField(max_length=255)
    heuredep = models.DateTimeField()
    heurearriver = models.DateTimeField()
    place = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    idModeTransport = models.ForeignKey(ModeDeTransport, on_delete=models.CASCADE)
    
class Herbergement(models.Model):
    adresse = models.CharField(max_length=255, null=True)
    ville = models.CharField(max_length=255, null=True)
    cp = models.CharField(max_length=255, null=True)
    prixNuit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField(null=True)

class Reservation(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, null=True)
    herbergement = models.ForeignKey(Herbergement, on_delete=models.CASCADE, null=True)
    payer = models.IntegerField(default=0, null=True)
    type = models.IntegerField(null=True)

