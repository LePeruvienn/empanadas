"""
URL configuration for tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from empanadas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path( 'empanadas/', views.empanadas),
    path( 'empanadas/<int:empanada_id>', views.empanada),
    path( 'empanadas/<int:empanada_id>/addIngredient', views.ajouterIngredientsEmpanada),
    path( 'ingredients/', views.ingredients),
    path( 'ingredients/add', views.formulaireCreationIngredient),
    path( 'ingredients/create', views.creerIngredient),
    path( 'empanadas/add', views.formulaireCreationEmpanada),
    path( 'empanadas/create', views.creerEmpanada),
    path('empanadas/<int:empanada_id>/delete/', views.supprimerEmpanada),
    path('empanadas/<int:empanada_id>/update/', views.afficherFormulaireModificationEmpanada), 
]
