from django.shortcuts import redirect, render
from empanadas.models import Empanada
from empanadas.models import Ingredient
from empanadas.models import Composition
from comptes.models import TiendaUser
from empanadas.forms import IngredientForm
from empanadas.forms import EmpanadaForm
from empanadas.forms import CompositionForm
from django.contrib.auth.models import User
from comptes.models import TiendaUser

# Create your views here.

# "/empanadas" request
def empanadas(request):
    user = None
    lesEmpanadas = Empanada.objects.all()
    if request.user.is_authenticated:
        user = TiendaUser.objects.get(id=request.user.id)
    return render(
            request,
            'empanadas/empanadas.html',
            {
                'empanadas' : lesEmpanadas,
                'user' : user,
            }
    )

# "/ingredients" request
def ingredients(request):
    user = None
    if request.user.is_staff:
        lesIngredients = Ingredient.objects.all()
        user = TiendaUser.objects.get(id=request.user.id)
        return render(
                request,
                'empanadas/ingredients.html',
                {
                    'ingredients': lesIngredients,
                    'user': user,
                }
        )
    elif request.user.is_authenticated:
        return redirect('/empanadas')
    else:
        return redirect('/login')


# "/ingredients" request
def empanada(request, empanada_id):
    lesIngredients = Ingredient.objects.all()
    laEmpanada = Empanada.objects.get( idEmpanada = empanada_id )
    compo = Composition.objects.filter (empanada = empanada_id)
    return render(
            request,
            'empanadas/empanada.html',
            {
                'ingredients' : lesIngredients,
                'empanada' : laEmpanada,
                'composition' : compo,
                'user' : TiendaUser.objects.get(id=request.user.id),
            }
    )

def formulaireCreationIngredient(request):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    return render (
        request,
        'empanadas/formulaireCreationIngredient.html',
        {
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )

def creerIngredient(request):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

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
                    'user' : TiendaUser.objects.get(id=request.user.id),
                }
        )
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            {
                'erreurs' : form.errors,
                'user' : TiendaUser.objects.get(id=request.user.id),
            },
        )

def formulaireCreationEmpanada(request):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    return render (
        request,
        'empanadas/formulaireCreationEmpanada.html',
        {
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )

def creerEmpanada(request):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

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
                    'user' : TiendaUser.objects.get(id=request.user.id),
                }
        )
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            {
                'erreurs' : form.errors,
                'user' : TiendaUser.objects.get(id=request.user.id),
            },
        )

def ajouterIngredientsEmpanada(request,empanada_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    form = CompositionForm(request.POST)
    if form.is_valid():
        ingr = form.cleaned_data['ingredient']
        qt = form.cleaned_data['quantite']
        emp = Empanada.objects.get(idEmpanada=empanada_id)
        recherche = Composition.objects.filter(
                    empanada=empanada_id,
                    ingredient=ingr.idIngredient,
                )
        if recherche.count() > 0:
            ligne = recherche.first()
        else:
            ligne = Composition()
            ligne.ingredient = ingr
            ligne.empanada = emp
        ligne.quantite = qt
        ligne.save()
        return redirect('/empanadas/%d' % empanada_id)
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            {
                'erreurs' : form.errors,
                'user' : TiendaUser.objects.get(id=request.user.id),
            }
        )


def supprimerEmpanada(request, empanada_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    lesEmpanadas = Empanada.objects.all()
    laEmpanada = Empanada.objects.get( idEmpanada = empanada_id )
    laEmpanada.delete()
    return render (
        request,
        'empanadas/empanadas.html',
        {
            'empanadas' : lesEmpanadas,
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )

def afficherFormulaireModificationEmpanada(request, empanada_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    laEmpanada = Empanada.objects.get( idEmpanada = empanada_id )
    return render (
        request,
        'empanadas/formulaireModificationEmpanada.html',
        {
            'empanada' : laEmpanada,
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )

def modifierEmpanada(request, empanada_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    empd = Empanada.objects.get( idEmpanada = empanada_id )
    form = EmpanadaForm(request.POST, request.FILES, instance = empd)
    if form.is_valid():
        nomEmpd = form.cleaned_data['nomEmpanada']
        prixEmpd = form.cleaned_data['prix']
        empd.nomEmpanada = nomEmpd
        empd.prix = prixEmpd
        if 'image' in request.FILES:
            empd.image = request.FILES['image']
        empd.save()
        return empanadas(request)
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            {
                'erreurs' : form.errors,
                'user' : TiendaUser.objects.get(id=request.user.id),
            },
        )


def afficherFormulaireModificationIngredient(request, ingredient_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    leIngredient = Ingredient.objects.get( idIngredient = ingredient_id )
    return render (
        request,
        'empanadas/formulaireModificationIngredient.html',
        {
            'ingredient' : leIngredient,
            'user' : TiendaUser.objects.get(id=request.user.id),
        }
    )


def modifierIngredient(request, ingredient_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    ingr = Ingredient.objects.get( idIngredient = ingredient_id )
    form = IngredientForm(request.POST, instance = ingr)
    if form.is_valid():
        nomIngr = form.cleaned_data['nomIngredient']
        ingr.nomIngredient = nomIngr
        ingr.save()
        return ingredients(request)
    else:
        return render (
            request,
            'empanadas/formulaireNonValide.html',
            {
                'erreurs' : form.errors,
                'user' : TiendaUser.objects.get(id=request.user.id),
            },
        )


def supprimerIngredient(request, ingredient_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    leIngredient = Ingredient.objects.all()
    leIngredient = Ingredient.objects.get( idIngredient = ingredient_id )
    leIngredient.delete()
    return ingredients(request)

def supprimerIngredientDansEmpanada(request, empanada_id, ing_id):
    # Check if user have permissions
    if not request.user.is_staff:
        if request.user.is_authenticated:
            return redirect('/empanadas')
        else:
            return redirect('/login')

    compo = Composition.objects.get(
                empanada=empanada_id,
                ingredient=ing_id,
    )
    compo.delete()
    return redirect('/empanadas/%d' % empanada_id)
