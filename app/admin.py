from django.contrib import admin
from .models import Acao, AcaoFavoritada 
# Removi "Contato" e "Usuario" da importação acima

@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'nome_empresa', 'setor', 'variacao')
    search_fields = ('ticket', 'nome_empresa')

@admin.register(AcaoFavoritada)
class AcaoFavoritadaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao')
    list_filter = ('usuario',)