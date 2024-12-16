from django.shortcuts import redirect, render
from paniers.models import Commande
from paniers.models import LigneCommande
from comptes.models import TiendaUser
from empanadas.models import Empanada

# Create your views here.

def afficherPanier(request):
    user = None
    if request.user.is_authenticated:
        panier = None
        lignes = None
        total = 0
        user = TiendaUser.objects.get(id = request.user.id)
        non_payees = Commande.objects.filter( user = user, payee = False ) 

        if len(non_payees) > 0:
            panier = non_payees[0]
            total = panier.prix
            lignes = LigneCommande.objects.filter(commande_id = panier.idCommande)

        return render(
                request,
                'paniers/panier.html',
                {
                    'lignes' : lignes,
                    'total' : total,
                    'user' : TiendaUser.objects.get(id=request.user.id),
                }
        )
    else:
        return redirect ('/login')

def ajouterEmpanadaAuPanier(request, empanada_id):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    empanada = Empanada.objects.get(idEmpanada=empanada_id)
    user = TiendaUser.objects.get(id=request.user.id)
    # On créer la commande ou on la récupère et on lui rajoute la empanada
    panier, _ = Commande.objects.get_or_create(user=user, payee=False, defaults={"prix": 0})
    panier.prix = panier.prix + empanada.prix
    panier.save()
    # On créer une ligne de la commande ou on la récupère
    ligne, _ = LigneCommande.objects.get_or_create(commande=panier, empanada=empanada, defaults={"quantite": 0, "prix": 0})
    ligne.quantite = ligne.quantite + 1
    ligne.prix = ligne.prix + empanada.prix
    ligne.save()
    # On affiche le panier
    return redirect ('/cart')

def retirerDuPanier(request, empanada_id):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    empanada = Empanada.objects.get(idEmpanada=empanada_id)
    user = TiendaUser.objects.get(id=request.user.id)
    # On récupère la commande en cours du client
    panier = None
    panier = Commande.objects.get(user=user, payee=False)
    # On arrête tout si le panier existe pas 
    if panier is not None:
        # On récupère la ligne du panier
        ligne = None
        ligne = LigneCommande.objects.get(commande=panier, empanada=empanada)
        # On arrête tout si la ligne existe pas 
        if ligne is not None:
            # On retire la valeurs de la ligne du panier
            panier.prix = panier.prix - ligne.prix
            panier.save()
            # On supprime le panier
            ligne.delete()
    # On affiche le panier
    return redirect ('/cart')

def retirerUneEmpanadaDuPanier(request, empanada_id):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    empanada = Empanada.objects.get(idEmpanada=empanada_id)
    user = TiendaUser.objects.get(id=request.user.id)
    # On récupère la commande en cours du client
    panier = None
    panier = Commande.objects.get(user=user, payee=False)
    # On arrête tout si le panier existe pas 
    if panier is not None:
        # On récupère la ligne du panier
        ligne = None
        ligne = LigneCommande.objects.get(commande=panier, empanada=empanada)
        # On arrête tout si la ligne existe pas 
        if ligne is not None:
            panier.prix = panier.prix - empanada.prix
            panier.save()
            if ligne.quantite > 1:
                ligne.quantite = ligne.quantite - 1
                ligne.prix = ligne.prix - empanada.prix
                ligne.save()
            else:
                return retirerDuPanier(request, empanada_id)
    # On affiche le panier
    return redirect ('/cart')

def viderPanier(request):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    user = TiendaUser.objects.get(id=request.user.id)
    # On récupère la commande en cours du client
    panier = None
    panier = Commande.objects.get(user=user, payee=False)
    # On arrête tout si le panier existe pas 
    if panier is not None:
        panier.delete()
    # On affiche le panier
    return redirect('/cart')

def payerPanier(request):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    user = TiendaUser.objects.get(id=request.user.id)
    # On récupère la commande en cours du client
    panier = None
    panier = Commande.objects.get(user=user, payee=False)
    # On arrête tout si le panier existe pas 
    if panier is not None:
        panier.payee = True
        panier.save()
        return render (
            request,
            'paniers/avisPaiement.html',
            {
                'user' : TiendaUser.objects.get(id=request.user.id),
            }
        )
    return redirect('/cart')

def afficherCommandes(request):
    # Si le user est pas connecté on le redirige vers son panier
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On récupère les données
    user = TiendaUser.objects.get(id=request.user.id)
    # On récupère la commande en cours du client
    commandes = []
    commandes = Commande.objects.filter(user=user, payee=True)
    # On arrête tout si le panier existe pas 
    return render(
        request,
        'paniers/commandes.html',
        {
            'commandes' : commandes,
            'total' : sum(commande.prix for commande in commandes),
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )

def afficherCommande(request, commande_id):
    user = None
    # On arrete ici si le user est pas connecté
    if not request.user.is_authenticated:
        return redirect ('/login')
    # On initialise Commande
    commande = None
    # On récupère le user
    user = TiendaUser.objects.get(id = request.user.id)
    # On récupère la commande
    try:
        commande = Commande.objects.get(user = user, idCommande=commande_id) 
    # Si l'utilisateur ne poss-de pas cete commande alors on arrete la 
    except Commande.DoesNotExist:
        return redirect('/orders')
    # On récpère les différentes ligne de la commande
    lignes = LigneCommande.objects.filter(commande_id=commande_id)
    # On affiche la vue
    return render(
            request,
            'paniers/commande.html',
            {
                'lignes' : lignes,
                'prix_total' : commande.prix,
                'user' : TiendaUser.objects.get(id=request.user.id),
            }
    )
