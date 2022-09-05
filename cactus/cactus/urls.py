from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import obtain_auth_token

from .grapheneWrapper import LoggingGraphQLView

from banca.views.transactionView import my_image
import notifications.urls
from servicios.views import web_chat


urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(LoggingGraphQLView.as_view(graphiql=True))),
    path('api/', include('banca.urls')),
    path('api/', include('demograficos.urls')),
    path('api/token-auth/', csrf_exempt(obtain_auth_token),
         name='api_token_auth'),
    path('qr/', my_image, name='qr'),
    url('^inbox/notifications/', include(notifications.urls,
                                         namespace='notifications')),
    path('', include('scotiabank.urls')),
    path("chat/", web_chat),
    path('', include('demograficos.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
