from django.contrib import admin

from .models import Question, Choice

# en el argumento de ChoiceInLine va la vista


class ChoiceInLine(admin.TabularInline):  # admin.StackedInLine
    model = Choice  # Modelo exportado de choice
    extra = 3  # Extra Choices


class QuestionAdmin(admin.ModelAdmin):
    # select the order of the fields.
    """
    fields = ['pub_date', 'question_text']
    """
    # separate the fields by name
    fieldsets = [
            (None,               {'fields': ['question_text']}),
            ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInLine]  # En lineas, marcar choice en lineas
    # Mostrar campos en el index
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']  # fecha de publicacion
    search_fields = ['question_text']  # barra de busqueda


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
