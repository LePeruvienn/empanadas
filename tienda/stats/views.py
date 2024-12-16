from django.shortcuts import render, redirect
from comptes.models import TiendaUser
from paniers.models import Commande, LigneCommande
from math import ceil

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
            'clients' : clients,
            'user' : TiendaUser.objects.get(id=request.user.id),
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
            'commandes' : commandes,
            'user' : TiendaUser.objects.get(id=request.user.id),
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
            'commande' : commande,
            'user' : TiendaUser.objects.get(id=request.user.id),
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
            'username' : username,
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )



def revenus (request):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login') # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')

    requete = """
        SELECT *
        FROM paniers_commande
        WHERE payee = 1
        and julianday (date()) - julianday (dateCommande) <= 7
        ORDER BY dateCommande
    """
    dernieresCommandes = Commande.objects.raw (requete)
    datesCommandes = []
    montantsCommandes = []
    for cmd in dernieresCommandes:
        date = cmd.dateCommande.strftime( '%d/%m/%Y' )
        montant = float(cmd.prix)
        if date not in datesCommandes:
            datesCommandes.append(date)
            montantsCommandes.append(montant)
        else:
            idx= datesCommandes.index(date)
            montantsCommandes[idx] += montant

    chiffreAffaireMax = max( montantsCommandes, default=0 )
    graduationCA = ceil( chiffreAffaireMax//5 ) *5 +5
    # Affichage de la vue
    return render(
        request,
        'stats/revenus.html',
        {
            'user' : TiendaUser.objects.get(id=request.user.id),
            'dates' : datesCommandes,
            'montants' : montantsCommandes,
            'CAMX' : graduationCA,
            'commandes' : dernieresCommandes, #pour debug
        }
    )

def ventes (request):
    # Si le user est pas connecté on le redirige vers la page de connection
    if not request.user.is_authenticated:
        return redirect ('/login')
    # Si il est pas staff on le renvoie vers les empanada
    if not request.user.is_staff:
        return redirect ('/empanadas')

    requete = """
        SELECT *
        FROM paniers_commande
        WHERE payee = 1
        and julianday (date()) - julianday (dateCommande) <= 7
        ORDER BY dateCommande
    """
    dernieresCommandes = Commande.objects.raw (requete)
    nomsEmpanadas = []
    ventesEmpanadas = []
    for cmd in dernieresCommandes:
        lignes = cmd.lignecommande_set.all()
        for ligne in lignes:
            nom = ligne.empanada.nomEmpanada
            qt = ligne.quantite
            if nom not in nomsEmpanadas:
                nomsEmpanadas.append(nom)
                ventesEmpanadas.append(qt)
            else:
                idx = nomsEmpanadas.index(nom)
                ventesEmpanadas[idx] += qt
    # Affichage de la vue
    return render(
        request,
        'stats/ventes.html',
        {
            'user' : TiendaUser.objects.get(id=request.user.id),
            'noms' : nomsEmpanadas,
            'ventes' : ventesEmpanadas,
            'commandes' : dernieresCommandes, #pour debug
        }
    )
