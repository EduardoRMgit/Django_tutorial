from django.urls import path, include


urlpatterns = [
    path('rapydcollect/', include('pagos.rapydcollect.urls')),
]
