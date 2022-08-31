from django.urls import path
from demograficos.views import ImageDoc

urlpatterns = [
    path('sendimage/', ImageDoc.as_view()),
]
