from django.forms import ModelForm
from empanadas.models import Ingredient
from empanadas.models import Empanada
from empanadas.models import Composition


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nomIngredient']

#from django import forms
# class IngredientForm(forms.form):
#    nomIngredient = formsCharField( label='nom ingrédient', max_length=50)


class EmpanadaForm(ModelForm):
    class Meta:
        model = Empanada
        fields = ['nomEmpanada', 'prix']

class CompositionForm(ModelForm):
    class Meta:
        model = Composition
        fields = ['ingredient', 'quantite']
