from django.db import models
from django.contrib.auth.models import User # Importante

class Acao(models.Model):
    ticket = models.CharField(max_length=45)
    nome_empresa = models.CharField(max_length=100)
    setor = models.CharField(max_length=45)
    descricao = models.TextField()
    variacao = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.ticket} - {self.nome_empresa}"

class AcaoFavoritada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Usa o User do Django
    acao = models.ForeignKey(Acao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'acao')
        verbose_name = "Ação Favoritada"

    def __str__(self):
        return f"{self.usuario.username} favoritou {self.acao.ticket}"
