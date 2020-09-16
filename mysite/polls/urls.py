from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('details', views.details),
    path('result', views.result),
    path('vote', views.vote)
]