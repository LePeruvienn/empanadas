from django.conf import settings
from django.conf.urls.static import static
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
    path( 'ingredients/<int:ingredient_id>/update/', views.afficherFormulaireModificationIngredient),
    path( 'ingredients/<int:ingredient_id>/updated/', views.modifierIngredient),
    path( 'ingredients/<int:ingredient_id>/delete/', views.supprimerIngredient),
    path( 'empanadas/add', views.formulaireCreationEmpanada),
    path( 'empanadas/create', views.creerEmpanada),
    path('empanadas/<int:empanada_id>/delete/', views.supprimerEmpanada),
    path('empanadas/<int:empanada_id>/update/', views.afficherFormulaireModificationEmpanada), 
    path('empanadas/<int:empanada_id>/updated/', views.modifierEmpanada), 
    path('empanadas/<int:empanada_id>/deleteIngredient/<int:ing_id>/', views.supprimerIngredientDansEmpanada), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
