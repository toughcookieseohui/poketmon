from django.urls import path
from . import views

app_name = 'poketmon'
urlpatterns = [
    path("", views.main, name='main'),
    path("type/",views.type, name='type'),
    path("bmi/", views.bmi, name='bmi'),
    path("size/", views.size, name='size'),
]