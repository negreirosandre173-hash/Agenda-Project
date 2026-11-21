from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='agendamentos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.painel_admin, name='painel_admin'),
    
    # Serviços
    path('painel/servicos/', views.gerenciar_servicos, name='gerenciar_servicos'),
    path('painel/servicos/remover/<int:servico_id>/', views.desativar_servico, name='desativar_servico'),
    
    # Profissionais
    path('painel/profissionais/', views.gerenciar_profissionais, name='gerenciar_profissionais'),
    path('painel/profissionais/remover/<int:profissional_id>/', views.desativar_profissional, name='desativar_profissional'),
    path('painel/horarios/', views.gerenciar_horarios, name='gerenciar_horarios'),
    path('painel/horarios/remover/<int:horario_id>/', views.remover_horario, name='remover_horario'),

]
