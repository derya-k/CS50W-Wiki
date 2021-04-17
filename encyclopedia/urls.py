from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.results, name="results"),
    path("newpage",views.newpage, name="newpage"),
    path("error",views.error, name="error"),
    path("random",views.random,name="random"),
    path("edit", views.edit, name="edit"),
     path("search", views.search, name="search"),
   
    
]
