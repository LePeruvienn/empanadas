from django.shortcuts import render
from empanadas.models import Empanada
from empanadas.models import Ingredient
from empanadas.models import Composition

# Create your views here.

# "/empanadas" request
def empanadas(request):
    lesEmpanadas = Empanada.objects.all()
    return render(
            request,
            'empanadas/empanadas.html',
            {'empanadas' : lesEmpanadas}
            )

# "/ingredients" request
def ingredients(request):
    lesIngredients = Ingredient.objects.all()
    return render(
            request,
            'empanadas/ingredients.html',
            {'ingredients' : lesIngredients}
            )


# "/ingredients" request
def empanada(request, empanada_id):
    laEmpanada = Empanada.objects.get( idEmpanada = empanada_id )
    compo = Composition.objects.filter (empanada = empanada_id)
    return render(
            request,
            'empanadas/empanada.html',
            {
                'empanada' : laEmpanada,
                'composition' : compo 
            }
    )
