from django.forms import ModelForm
from empanadas.models import Ingredient


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nomIngredient']

#from django import forms
# class IngredientForm(forms.form):
#    nomIngredient = formsCharField( label='nom ingrédient', max_length=50)
