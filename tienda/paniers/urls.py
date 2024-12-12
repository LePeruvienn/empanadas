from django.urls import path
from django.contrib.auth import views as auth_views
from paniers import views

urlpatterns = [
    path('orders', views.afficherCommandes),
    path('orders/<int:commande_id>', views.afficherCommande),
    path('cart', views.afficherPanier),
    path('cart/<int:empanada_id>/buy/', views.ajouterEmpanadaAuPanier),
    path('cart/<int:empanada_id>/delete/', views.retirerDuPanier),
    path('cart/<int:empanada_id>/decrease/', views.retirerUneEmpanadaDuPanier),
    path('cart/delete/', views.viderPanier),
    path('cart/pay/', views.payerPanier),
]
