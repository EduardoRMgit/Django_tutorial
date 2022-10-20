from django.contrib import admin
from dapp.models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = [
        'category',
        'name'
    ]


admin.site.register(Category, CategoryAdmin)
