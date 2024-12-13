from django.shortcuts import render, redirect
from comptes.models import TiendaUser
from paniers.models import Commande, LigneCommande

# Create your views here.

def clients(request):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login')
    # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')

    # On récupère les données
    clients = TiendaUser.objects.filter(is_staff = False).order_by('date_joined')
    # On affiche la vue et on passes les utilisateurs en paramètre
    return render(
        request,
        'stats/clients.html',
        {
            'clients' : clients
        }
    )

def commandes(request):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login')
    # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')
    
    commandes = []
    commandes = Commande.objects.filter(payee = True).order_by('dateCommande')
    for commande in commandes:
        commande.client = TiendaUser.objects.get(id=commande.user.id)
    return render(
        request,
        'stats/commandes.html',
        {
            'commandes' : commandes
        }
    )

def commande(request, commande_id):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login')
    # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')

    commande = Commande.objects.get(idCommande=commande_id)
    lignes = []
    lignes = LigneCommande.objects.filter(commande=commande)
    return render(
        request,
        'stats/commande.html',
        {
            'lignes' : lignes,
            'commande' : commande
        }
    )

def commandes_client(request,client_id):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login')
    # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')

    # On récupère les données
    user = TiendaUser.objects.get(id=client_id)
    username = user.username
    # On récupère la commande en cours du client
    commandes = []
    commandes = Commande.objects.filter(user=user, payee=True)
    # On met en places les lignes de la commande
    for commande in commandes:
        commande.lignes = []
        commande.lignes = LigneCommande.objects.filter(commande=commande)
    # On arrête tout si le panier existe pas 
    return render(
        request,
        'stats/commandes_client.html',
        {
            'commandes' : commandes,
            'username' : username
        }
    )
