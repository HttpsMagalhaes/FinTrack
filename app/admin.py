# app/admin.py
from django.contrib import admin
from .models import Usuario, Acao, AcaoFavoritada, Contato

admin.site.register(Usuario)
admin.site.register(Acao)
admin.site.register(AcaoFavoritada)
admin.site.register(Contato)
