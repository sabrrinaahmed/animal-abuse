from django.urls import path
from . import views

urlpatterns = [
    path('', views.newsPage, name="newsPage"),

]