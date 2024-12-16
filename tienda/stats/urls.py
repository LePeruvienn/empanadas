from django.contrib import admin
from django.urls import path
from django.urls import path
from stats import views

urlpatterns = [
    path('clients/', views.clients),
    path('commandes/', views.commandes),
    path('commandes/<int:commande_id>', views.commande),
    path('clients/<int:client_id>', views.commandes_client),
    path('revenus/', views.revenus),
    path('ventes/', views.ventes),
]
