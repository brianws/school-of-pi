from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.sus_list, name='sus_list'),
    path('schoolofpi/schools/', views.schools, name='schools'),
    path('schoolofpi/score/<int:pk>', views.score, name='score'),
    path('schoolofpi/areas/<int:pk>', views.sus_list, name='sus_list'),
]