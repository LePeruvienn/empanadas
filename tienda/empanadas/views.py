from django.shortcuts import render
from empanadas.models import Empanada
from empanadas.models import Ingredient

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
