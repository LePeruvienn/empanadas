from django.db import models

# Create your models here.

### CLASSE INGREDIENT
class Ingredient(models.Model):
    # clé primaire, avec auto incrémentation
    idIngredient = models.AutoField( primary_key = True )
    # chaine de caractre de taille bornee
    nomIngredient = models.CharField( max_length = 50 )
    # version python du toString(), utilise par django dans ses interfaces
    def __str__(self) :
        return self.nomIngredient


### CLASSE EMPANADA
class Empanada(models.Model):
    # clé primaire, avec auto incrémentation
    idEmpanada = models.AutoField( primary_key = True )
    # chaine de caractre de taille bornee
    nomEmpanada = models.CharField( max_length = 50 )
    # nombre decimal, max 6 chiffres dont 2 après la virgule
    prix = models.DecimalField( max_digits = 6, decimal_places = 2 )
    # version python du toString(), utilise par django dans ses interfaces
    def __str__(self) :
        return self.nomEmpanada

### CLASSE EMPANADA
class Composition(models.Model):
    class Meta: # classe qui fait la liason
        unique_together = ('ingredient', 'empanada')
    # clées primaire, avec auto incrémentation
    idComposition = models.AutoField( primary_key = True )
    # clées étrangères
    ingredient = models.ForeignKey( Ingredient, on_delete = models.CASCADE )
    empanada = models.ForeignKey( Empanada, on_delete = models.CASCADE )
    # quantité de l'ingrédient
    quantite = models.CharField( max_length = 100)
    # version python du toString(), utilise par django dans ses interfaces
    def __str__(self) :
        res = self.ingredient.nomIngredient+ ' fait partie de la empanada' \
            + ' "'+self.empanada.nomEmpanada+'"' \
            + ' (quantité: '+self.quantite+')'
        return res
