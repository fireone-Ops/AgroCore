from django.urls import path
from . import views

urlpatterns = [
    # Maquinarios
    path('maquinarios/', views.CriarMaquinarioView.as_view(), name='criar-maquinario'),
    path('maquinarios/<int:pk>/', views.ListarMaquinariosView.as_view(), name='listar-maquinario'),
    
    # Manutencoes
    path('manutencoes/', views.CriarManutencaoView.as_view(), name='criar-manutencao'),
    path('manutencoes/<int:pk>/', views.ListarManutencaoView.as_view(), name='listar-manutencao'),
    
    # Telemetrias
    path('telemetrias/', views.CriarTelemetriaView.as_view(), name='criar-telemetria'),
    path('telemetrias/<int:pk>/', views.ListarTelemetriaView.as_view(), name='listar-telemetria'),
    
    # Atividades
    path('atividades/', views.CriarAtividadeView.as_view(), name='criar-atividade'),
    path('atividades/<int:pk>/', views.ListarAtividadeView.as_view(), name='listar-atividade'),
]
