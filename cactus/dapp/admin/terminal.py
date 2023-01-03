from django.contrib import admin
from dapp.models import Terminal


class TerminalAdmin(admin.ModelAdmin):
    model = Terminal
    list_display = [
        'id',
        'employee',
        'name'
    ]


admin.site.register(Terminal, TerminalAdmin)
