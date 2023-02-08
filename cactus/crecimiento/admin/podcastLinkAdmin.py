from django.contrib import admin
from crecimiento.models import PodcastLink


class PodcastLinkAdmin(admin.ModelAdmin):

    model = PodcastLink

    fields = [f.name for f in PodcastLink._meta.fields]
    fields.remove("id")
    list_display = fields
    search_fields = (
        'nombre',
    )


admin.site.register(PodcastLink, PodcastLinkAdmin)
