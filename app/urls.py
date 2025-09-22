from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hor/<int:year>/', views.hor_home, name='hor_home'),
    path('hor/<int:year>/parties', views.hor_parties, name='hor_parties'),
    path('hor/<int:year>/constituencies', views.hor_constituencies, name='hor_constituencies'),
]