from django.contrib import admin
from demograficos.models import UserLocation, UDevice


class UserLocationAdmin(admin.ModelAdmin):

    list_display = ('user',
                    'location',
                    'date')

    search_fields = ('user__username',)


admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(UDevice)
