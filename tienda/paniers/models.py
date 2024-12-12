from django.db import models
from datetime import date
from comptes.models import TiendaUser
from empanadas.models import Empanada

# Create your models here.

### CLASSE EMPANADA
class Commande(models.Model):
    # clé primaire, avec auto incrémentation
    idCommande = models.AutoField( primary_key = True )
    # date à laquelle la commande à été passée
    dateCommande = models.DateField(default=date.today)
    # Statut de la commande (payée / pas payée)
    payee = models.BooleanField(default=False)
    # nombre decimal, max 6 chiffres dont 2 après la virgule
    prix = models.DecimalField( max_digits = 6, decimal_places = 2 )
    # Id de l'utilisateur qui as passé la commande
    user = models.ForeignKey( TiendaUser, on_delete = models.CASCADE )
    # version python du toString(), utilise par django dans ses interfaces
    def __str__(self) :
        return 'commande ' + str(self.idCommande) + ' effectué le ' + str(self.dateCommande) + ' (prix ' + str(self.prix) + '€ )'

### LIGNE COMMANDE
class LigneCommande(models.Model):
    # clé primaire, avec auto incrémentation
    idLigneCommande = models.AutoField( primary_key = True )
    # quantite de l'empanada
    quantite = models.IntegerField()
    # nombre decimal, max 6 chiffres dont 2 après la virgule
    prix = models.DecimalField( max_digits = 6, decimal_places = 2 )
    # Id de la commande associée
    commande = models.ForeignKey( Commande, on_delete = models.CASCADE )
    # Id de l'empanada associée
    empanada = models.ForeignKey( Empanada, on_delete = models.CASCADE )
    # version python du toString(), utilise par django dans ses interfaces
    def __str__(self) :
        return 'Ligne commande ' + str(self.idLigneCommande) + ' de la commande ' + str(self.commande_id)
