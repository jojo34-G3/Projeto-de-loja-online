from django import forms
from .models import user, produto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class userform(forms.ModelForm):
    class Meta:
        model = user
        fields = ['username', 'password', 'email', 'telefone', 'data_de_nascimento', 'cpf', 'rg', 'endereco', 'cidade', 'estado', 'cep']



class produtoform(forms.ModelForm):
    class Meta:
        model = produto
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'imagem', 'categoria']  # Não inclua 'criado_por'



class registroform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']  # Removido 'email2'