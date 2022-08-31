from django.contrib import admin

from demograficos.models.userProfile import (StatusRegistro,
                                             StatusCuenta)
from demograficos.models.profileChecks import ProfileComponent
from demograficos.models.documentos import DocExtraction

admin.site.register(StatusRegistro)
admin.site.register(StatusCuenta)
admin.site.register(ProfileComponent)
admin.site.register(DocExtraction)
