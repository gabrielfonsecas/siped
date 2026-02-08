"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.conf.urls import handler404, handler500
from core import views
from core.views import menu, cadastro, nova_consulta, consultas, pacientes, apagar_paciente, editar_paciente


urlpatterns = [
    path('', views.IndexView.as_view(template_name='core/index.html'), name='index.html'),
    path('verificar_cpf/', views.verificar_cpf, name='verificar_cpf'),
    path('verificar_cpf_responsavel/', views.verificar_cpf_responsavel, name='verificar_cpf_responsavel'),
    path('menu/', login_required(menu), name='menu.html'),
    path('cadastro/', cadastro, name='cadastro'),
    path('nova_consulta/', nova_consulta, name='nova_consulta'),
    path('consultas/', consultas, name='consultas'),
    path('pacientes/', pacientes, name='pacientes'),
    path('apagar_paciente/<int:id_paciente>/',
         apagar_paciente, name='apagar_paciente'),
    path('editar_paciente/<int:id_paciente>/',
         editar_paciente, name='editar_paciente'),   
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
]


handler404 = 'core.views.custom_404'

handler500 = 'core.views.custom_500'
"""
from django.contrib import admin
from django.urls import path
from core.views import index, menu, cadastroPaciente, paciente, paciente_view, editarPaciente, excluirPaciente, novaConsulta, consulta_view,listar_consultas, grafico_crescimento,listar_pacientes, nova_consulta_listar_pacientes, listar_paciente_grafico
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index.as_view(template_name='core/index.html'), name='index.html'),
    path('menu/', login_required(menu), name='core/menu.html'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('cadastro-paciente/', cadastroPaciente, name='cadastroPaciente'),
    path('paciente/', listar_pacientes, name='paciente'),
    path('listar-pacientes/', listar_pacientes, name='listar_pacientes'),
    path('paciente/<int:id_paciente>/', paciente_view, name='paciente'),#url com id do paciente 
    path('paciente/editar/<int:id_paciente>/', editarPaciente, name='editarPaciente'),
    path('paciente/excluir/<int:id_paciente>/', excluirPaciente, name='excluirPaciente'),
    path('novaConsulta/', nova_consulta_listar_pacientes, name='nova_consulta_listar_pacientes'),
    path('novaConsulta/listar-pacientes/', nova_consulta_listar_pacientes, name='nova_consulta_listar_pacientes'),
    path('novaConsulta/<int:id_paciente>/', novaConsulta, name='novaConsulta'),
    path('consulta/<int:consulta_id>/', consulta_view, name='consulta'),
    path('consulta/', listar_consultas, name='listar_consultas'),
    path('grafico-crescimento/listar-pacientes/', listar_paciente_grafico, name='listar_paciente_grafico'),
    path('grafico-crescimento/<int:id_paciente>/', grafico_crescimento, name='grafico_crescimento'),
    





]
