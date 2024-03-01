
from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("inscription", views.inscription, name="inscription"),
    path("connexion", views.connexion, name="connexion"),
    path('logout/', views.logout, name='logout'),
    path("voyages", views.voyages, name="voyages" ),
    path("hebergements", views.hebergements, name="hebergements"),
    path('reserver_voyage/<int:voyage_id>/', views.reserver_voyage, name='reserver_voyage'),
    path('reservations_utilisateur/', views.reservations_utilisateur, name='reservations_utilisateur'),
    path('reserver_hebergement/<int:hebergement_id>/', views.reserver_hebergement, name='reserver_hebergement'),
    path('payer_reservation/<int:reservation_id>/', views.payer_reservation, name='payer_reservation'),

]

