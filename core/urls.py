from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path(
        'aprendizados-profissionais/<slug:slug>/',
        views.empresa_profissional_detail,
        name='empresa_profissional_detail',
    ),
    path('aprendizados/<slug:slug>/', views.tema_estudo_detail, name='tema_estudo_detail'),
    path(
        'aprendizados/<slug:tema_slug>/<slug:slug>/',
        views.publicacao_estudo_detail,
        name='publicacao_estudo_detail',
    ),
]
