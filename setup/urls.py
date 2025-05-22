"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import render
from django.urls import path
from app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_redirect, name='home'),  # Página inicial vai para registro
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/deletar/', views.produto_delete, name='produto_delete'),
    path('produtos/<int:pk>/favoritar/', views.favoritar_produto, name='favoritar_produto'),
    path('produtos/<int:pk>/comprar/', views.comprar_produto, name='comprar_produto'),
    path('produtos/<int:pk>/', views.produto_detail, name='produto_detail'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/perfil/', views.perfil_cliente, name='perfil_cliente'),  # Adicione esta linha
    path('clientes/<int:pk>/foto/', views.atualizar_foto_perfil, name='atualizar_foto_perfil'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/excluir/', views.cliente_delete, name='cliente_delete'),
    path('clientes/<int:pk>/entrar/', views.cliente_login_instant, name='cliente_login_instant'),
    path('admin-produtos/', views.admin_produtos, name='admin_produtos'),
    path('ofertas/', views.ofertas_magalu, name='ofertas_magalu'),
    path('produtos/<int:pk>/oferta-adicionar/', views.adicionar_oferta_magalu, name='adicionar_oferta_magalu'),
    path('produtos/<int:pk>/oferta-remover/', views.remover_oferta_magalu, name='remover_oferta_magalu'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
