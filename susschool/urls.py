from django.urls import path
from . import views

urlpatterns = [
    path('', views.schools, name='schools'),
    path('schoolofpi/schools/', views.schools, name='schools'),
    path('schoolofpi/score/<int:pk>', views.score, name='score'),
    path('schoolofpi/areas/<int:pk>', views.areas, name='areas'),
]