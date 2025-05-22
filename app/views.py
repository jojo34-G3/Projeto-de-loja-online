from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import produto, user
from .forms import produtoform, registroform, userform
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

def registro(request):
    if request.method == 'POST':
        form = registroform(request.POST)
        if form.is_valid():
            user_auth = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            # Crie o user do seu model customizado
            user_obj = user.objects.create(
                id=user_auth.id,
                username=username,
                password=password,
                email=email,
                telefone='',
                data_de_nascimento='2000-01-01',
                cpf='',
                rg='',
                endereco='',
                cidade='',
                estado='',
                cep=''
            )
            user_auth = authenticate(username=username, password=password)
            login(request, user_auth)
            messages.success(request, 'Registro realizado com sucesso!')

            # Envia e-mail de confirmação
            subject = 'Conta criada com sucesso'
            message = f'Olá, {username}!\n\nSua conta foi criada com sucesso.\n\nUsuário: {username}\nSenha: {password}\n\nGuarde estas informações com segurança.'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost')
            try:
                send_mail(subject, message, from_email, [email], fail_silently=False)
            except Exception as e:
                messages.error(request, f'Erro ao enviar e-mail: {e}')

            return redirect('produto_list')
    else:
        form = registroform()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('produto_list')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def produto_list(request):
    cliente_logado = None
    if request.user.is_authenticated:
        try:
            cliente_logado = user.objects.get(pk=request.user.id)
        except user.DoesNotExist:
            cliente_logado = None
    # Mostra apenas produtos criados pelo usuário autenticado
    produtos = produto.objects.filter(criado_por=cliente_logado)
    return render(request, 'produto_list.html', {'produtos': produtos, 'cliente_logado': cliente_logado})

def cliente_list(request):
    clientes = user.objects.all()
    cliente_logado = None
    if request.user.is_authenticated:
        try:
            cliente_logado = user.objects.get(pk=request.user.id)
        except user.DoesNotExist:
            cliente_logado = None
    return render(request, 'cliente_list.html', {'clientes': clientes, 'cliente_logado': cliente_logado})

def cliente_create(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = userform()
    return render(request, 'cliente_form.html', {'form': form})

def produto_create(request):
    if request.method == 'POST':
        form = produtoform(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.criado_por = user.objects.get(pk=request.user.id)
            prod.save()
            form.save_m2m()
            return redirect('produto_list')
    else:
        form = produtoform()
    return render(request, 'produto_form.html', {'form': form})

def produto_update(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    if request.method == 'POST':
        form = produtoform(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = produtoform(instance=prod)
    return render(request, 'produto_form.html', {'form': form})

def produto_delete(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    if request.method == 'POST':
        prod.delete()
        return redirect('produto_list')
    return render(request, 'produto_confirm_delete.html', {'produto': prod})

@require_POST
@login_required
def favoritar_produto(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    try:
        cliente = user.objects.get(pk=request.user.id)
    except user.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')
    # Só altera favoritos do usuário autenticado
    if prod in cliente.favoritos.all():
        cliente.favoritos.remove(prod)
    else:
        cliente.favoritos.add(prod)
    return redirect('perfil_cliente', pk=cliente.pk)

@require_POST
@login_required
def comprar_produto(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    try:
        cliente = user.objects.get(pk=request.user.id)
    except user.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')
    # Só altera compras do usuário autenticado
    cliente.compras.add(prod)
    return redirect('perfil_cliente', pk=cliente.pk)

@login_required
def atualizar_foto_perfil(request, pk):
    if request.user.id != pk:
        messages.error(request, "Acesso negado.")
        return redirect('perfil_cliente', pk=request.user.id)
    cliente = get_object_or_404(user, pk=pk)
    if request.method == 'POST':
        imagem = request.FILES.get('imagem')
        if imagem:
            cliente.imagem = imagem
            cliente.save()
        return redirect('perfil_cliente', pk=pk)
    return render(request, 'atualizar_foto_perfil.html', {'cliente': cliente})

@login_required
def perfil_cliente(request, pk):
    # Sempre mostra o perfil do usuário autenticado, nunca de outro
    if request.user.id != pk:
        messages.error(request, "Acesso negado. Você só pode acessar seu próprio perfil.")
        return redirect('perfil_cliente', pk=request.user.id)
    try:
        cliente = user.objects.get(pk=request.user.id)
    except user.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
        return redirect('cliente_list')
    # Mostra apenas compras/favoritos do usuário autenticado
    compras = cliente.compras.filter(comprado_por=cliente)
    favoritos = cliente.favoritos.filter(favoritado_por=cliente)
    categorias_compras = sorted(set(prod.categoria for prod in compras))
    categorias_favoritos = sorted(set(prod.categoria for prod in favoritos))
    return render(request, 'perfil_cliente.html', {
        'cliente': cliente,
        'compras': compras,
        'favoritos': favoritos,
        'categorias_compras': categorias_compras,
        'categorias_favoritos': categorias_favoritos,
    })

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(user, pk=pk)
    if request.method == 'POST':
        form = userform(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente atualizado com sucesso!")
            return redirect('cliente_list')
    else:
        form = userform(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(user, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, "Cliente excluído com sucesso!")
        return redirect('cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})

@require_POST
@login_required
def cliente_login_instant(request, pk):
    from django.contrib.auth.models import User as AuthUser
    try:
        auth_user = AuthUser.objects.get(pk=pk)
        login(request, auth_user)
        return redirect('perfil_cliente', pk=pk)
    except AuthUser.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('cliente_list')

def home_redirect(request):
    return redirect('registro')

@login_required
def admin_produtos(request):
    produtos = produto.objects.all()
    cliente_logado = None
    if request.user.is_authenticated:
        try:
            cliente_logado = user.objects.get(pk=request.user.id)
        except user.DoesNotExist:
            cliente_logado = None
    return render(request, 'admin_produtos.html', {'produtos': produtos, 'cliente_logado': cliente_logado})

def produto_detail(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    cliente_logado = None
    if request.user.is_authenticated:
        try:
            cliente_logado = user.objects.get(pk=request.user.id)
        except user.DoesNotExist:
            cliente_logado = None
    return render(request, 'produto_detail.html', {'produto': prod, 'cliente_logado': cliente_logado})

@require_POST
@login_required
def adicionar_oferta_magalu(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    prod.oferta_magalu = True
    prod.save()
    return redirect('ofertas_magalu')

@require_POST
@login_required
def remover_oferta_magalu(request, pk):
    prod = get_object_or_404(produto, pk=pk)
    prod.oferta_magalu = False
    prod.save()
    return redirect('ofertas_magalu')

def ofertas_magalu(request):
    produtos = produto.objects.filter(oferta_magalu=True)
    cliente_logado = None
    if request.user.is_authenticated:
        try:
            cliente_logado = user.objects.get(pk=request.user.id)
        except user.DoesNotExist:
            cliente_logado = None
    return render(request, 'ofertas_magalu.html', {'produtos': produtos, 'cliente_logado': cliente_logado})
