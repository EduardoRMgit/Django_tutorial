from django.urls import path
from pld.views import AlertasPLDView


urlpatterns = [
    path('alertapld/', AlertasPLDView.as_view())
]
