from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from . import models

# Create your views here.

def index(request):
    if request.session['prenom_utilisateur'] or request.session['prenom_utilisateur'] != '':
        return render(request, 'index.html')
    else:
        return redirect('connexion')

def inscription(request): 
    request.session['nom_utilisateur']=''
    request.session['prenom_utilisateur']='' 
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        adresse = request.POST['adress']
        mdp = request.POST['motDePase']
        utilisateur = models.Utilisateur.objects.create(nom=nom, prenom=prenom, tel=tel, adresse=adresse, mdp=mdp)
        return redirect('connexion')
    else:
        return render(request, 'inscription.html')

def connexion(request):
        if request.method == 'POST':
            prenom = request.POST['prenom']
            mdp = request.POST['mdp']

            try:
                utilisateur = models.Utilisateur.objects.get(prenom=prenom)
                if utilisateur.mdp == mdp:
                    request.session['prenom_utilisateur'] = utilisateur.prenom
                    request.session['nom_utilisateur'] = utilisateur.nom
                    return redirect('index')
                else:
                    messages.error(request, "Mot de passe incorrect ou Utilisateur non trouvé")
            except models.Utilisateur.DoesNotExist:
                messages.error(request, "Mot de passe incorrect ou Utilisateur non trouvé")

        return render(request, 'connexion.html')

def logout(request):
    # Supprimer les variables de session de l'utilisateur
    request.session['nom_utilisateur']=''
    request.session['prenom_utilisateur']='' 
    messages.error(request, '')
    
    # Rediriger vers la page de connexion
    return redirect('connexion')

def voyages(request):
        arriver = request.POST.get('arriver', None)
        if arriver:
            allVoyage = models.Voyage.objects.filter(arriver=arriver)
        else:
            allVoyage = models.Voyage.objects.all()
        return render(request, 'voyage.html', {'allVoyage': allVoyage})

def hebergements(request):
        ville = request.POST.get('ville', None)
        if ville:
            allHebergements = models.Herbergement.objects.filter(ville=ville)
        else:
            allHebergements = models.Herbergement.objects.all()
        return render(request, 'hebergement.html', {'allHebergements': allHebergements})

from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

def reserver_hebergement(request, hebergement_id):
    if request.method == 'POST':
        # Vérifiez si l'utilisateur est connecté
        if 'prenom_utilisateur' in request.session and request.session['prenom_utilisateur']:
            # Récupérez l'hébergement correspondant à l'ID
            try:
                hebergement = models.Herbergement.objects.get(pk=hebergement_id)
            except models.Herbergement.DoesNotExist:
                messages.error(request, "L'hébergement n'existe pas")
                return redirect('hebergements')

            # Récupérez le nom de l'utilisateur connecté
            nom_utilisateur = request.session['nom_utilisateur']
            try:
                utilisateur = models.Utilisateur.objects.get(nom=nom_utilisateur)
            except models.Utilisateur.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé")
                return redirect('connexion')

            # Créez une réservation pour cet hébergement avec cet utilisateur
            reservation = models.Reservation.objects.create(user=utilisateur, herbergement=hebergement, payer=0, type=1)
            messages.success(request, "Réservation effectuée avec succès!")
            return redirect('index') 
        else:
            # Redirigez l'utilisateur vers la page de connexion s'il n'est pas connecté
            messages.error(request, "Veuillez vous connecter pour réserver un hébergement")
            return redirect('connexion')
    else:
        # Redirigez l'utilisateur vers la page d'accueil si la méthode de requête n'est pas POST
        return redirect('index')


        
def reserver_voyage(request, voyage_id):
        if request.method == 'POST':
            voyage = models.Voyage.objects.get(pk=voyage_id)
            nom_utilisateur = request.session.get('nom_utilisateur')
            if nom_utilisateur:
                try:
                    utilisateur = models.Utilisateur.objects.get(nom=nom_utilisateur)
                    models.Reservation.objects.create(user=utilisateur, voyage=voyage, payer=0, type=0)
                    return redirect('index') 
                except models.Utilisateur.DoesNotExist:
                    return redirect('connexion')
            else:
                return redirect('connexion')
        else:
            return redirect('index')

def reservations_utilisateur(request):
    nom_utilisateur = request.session.get('nom_utilisateur')
    if nom_utilisateur:
        try:
            reservations = models.Reservation.objects.filter(user__nom=nom_utilisateur)
            return render(request, 'reservation.html', {'reservations': reservations})
        except models.Reservation.DoesNotExist:
            return render(request, 'reservation.html', {'reservations': None})
    else:
        return redirect('connexion')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    

def payer_reservation(request, reservation_id):
    if request.method == 'POST':
        try:
            reservation = models.Reservation.objects.get(pk=reservation_id)
            # Mettre à jour la valeur de payer à 1
            reservation.payer = 1
            reservation.save()
        except models.Reservation.DoesNotExist:
            # Gérer l'erreur si la réservation n'existe pas
            pass
    return redirect('reservations_utilisateur')