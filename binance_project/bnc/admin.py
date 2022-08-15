from django.contrib import admin
from .models import Symbol


class SymbolAdmin(admin.ModelAdmin):
    list_display  = ('user')
    search_fields = ['user',]


admin.site.register(Symbol)
