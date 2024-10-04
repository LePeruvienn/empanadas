from django.shortcuts import render
from empanadas.models import Empanada
from empanadas.models import Ingredient
from empanadas.models import Composition
from empanadas.forms import IngredientForm
from empanadas.forms import EmpanadaForm

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

def formulaireCreationIngredient(request):
    return render (
            request,
            'empanadas/formulaireCreationIngredient.html'
            )

def creerIngredient(request):
    form = IngredientForm(request.POST)
    if form.is_valid():
        nomIngr = form.cleaned_data['nomIngredient']
        ingr = Ingredient()
        ingr.nomIngredient = nomIngr
        ingr.save()
        return render(
                request,
                'empanadas/traitementFormulaireCreationIngredient.html',
                {
                    'nom' : nomIngr,
                }
        )
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            { 'erreurs' : form.errors},
        )

def formulaireCreationEmpanada(request):
    return render (
            request,
            'empanadas/formulaireCreationEmpanada.html'
            )

def creerEmpanada(request):
    form = EmpanadaForm(request.POST)
    if form.is_valid():
        nomEmpd = form.cleaned_data['nomEmpanada']
        prixEmpd = form.cleaned_data['prix']
        empd = Empanada()
        empd.nomEmpanada = nomEmpd
        empd.prix = prixEmpd
        empd.save()
        return render(
                request,
                'empanadas/traitementFormulaireCreationEmpanada.html',
                {
                    'nom' : nomEmpd,
                    'prix' : prixEmpd,
                }
        )
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            { 'erreurs' : form.errors},
        )
