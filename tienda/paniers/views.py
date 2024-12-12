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
        user = TiendaUser.objects.get(id = request.user.id)
        non_payees = Commande.objects.filter( user = user ).filter( payee = False ) 

        if len(non_payees) > 0:
            panier = non_payees[0]
            lignes = LigneCommande.objects.filter(commande_id = panier.idCommande)

        return render(
                request,
                'paniers/panier.html',
                {
                    'lignes' : lignes
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
    panier, created = Commande.objects.get_or_create(user=user, payee=False, defaults={"prix": 0})
    panier.prix = panier.prix + empanada.prix
    panier.save()
    # On créer une ligne de la commande ou on la récupère
    ligne, created = LigneCommande.objects.get_or_create(commande=panier, empanada=empanada, defaults={"quantite": 0, "prix": 0})
    ligne.quantite = ligne.quantite + 1
    ligne.prix = ligne.prix + empanada.prix
    ligne.save()
    # On affiche le panier
    return redirect ('/cart')
