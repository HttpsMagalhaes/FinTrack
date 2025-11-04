from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=100, unique=True)
    senha = models.TextField()

    def __str__(self):
        return self.nome


class Acao(models.Model):
    ticket = models.CharField(max_length=45)
    nome_empresa = models.CharField(max_length=100)
    setor = models.CharField(max_length=45)
    descricao = models.TextField()
    variacao = models.FloatField(default=0.0)  # 🔹 novo campo

    def __str__(self):
        return f"{self.ticket} - {self.nome_empresa}"

class AcaoFavoritada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    acao = models.ForeignKey(Acao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'acao')  # Evita duplicatas
        verbose_name = "Ação Favoritada"
        verbose_name_plural = "Ações Favoritadas"

    def __str__(self):
        return f"{self.usuario.nome} tem {self.acao.ticket} como ação favorita"


class Contato(models.Model):
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=100)
    mensagem = models.TextField()

    def __str__(self):
        return f"Mensagem de {self.nome}"
