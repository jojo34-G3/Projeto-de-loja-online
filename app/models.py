from django.db import models

# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    cpf = models.CharField(max_length=100)
    rg = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='perfil/', blank=True, null=True)
    favoritos = models.ManyToManyField('produto', related_name='favoritado_por', blank=True)
    compras = models.ManyToManyField('produto', related_name='comprado_por', blank=True)

    def __str__(self):
        return self.username
    
    
class produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.CharField(max_length=100)
    oferta_magalu = models.BooleanField(default=False)
    criado_por = models.ForeignKey('user', on_delete=models.CASCADE, related_name='produtos_criados', null=True, blank=True)

    def __str__(self):
        return self.nome
