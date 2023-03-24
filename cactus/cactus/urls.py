from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from rest_framework.authtoken.views import obtain_auth_token

from .grapheneWrapper import LoggingGraphQLView

from banca.views.transactionView import my_image
import notifications.urls
from servicios.views import web_chat

from cactus.settings import SITE


if SITE in [
    "stage",
    "test",
    "prod"
]:
    from two_factor.urls import urlpatterns as tf_urls
    from two_factor.admin import (
        AdminSiteOTPRequired,
        AdminSiteOTPRequiredMixin
    )

    class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired):
        def login(self, request, extra_context=None):
            redirect_to = request.POST.get(
                REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME)
            )
            # Para los usuarios que aún no han verificado
            # el  AdminSiteOTPRequired.has_permission
            # fallará. Por lo tanto, use la verificación
            # estándar de administrador has_permission check:
            # (is_active and is_staff) y luego verifique la verificación.
            # Vaya al índice si aprueban, de lo contrario,
            # haga que configuren el dispositivo OTP.
            if request.method == "GET" and super(
                AdminSiteOTPRequiredMixin, self
            ).has_permission(request):
                # Ya iniciado sesión y verificado por OTP
                if request.user.is_verified():
                    # El usuario tiene permiso
                    index_path = reverse("admin:index", current_app=self.name)
                else:
                    # El usuario tiene permiso pero no se establece OTP:
                    index_path = reverse(
                        "two_factor:setup", current_app=self.name
                    )
                return HttpResponseRedirect(index_path)
            if not redirect_to or not url_has_allowed_host_and_scheme(
                url=redirect_to, allowed_hosts=[request.get_host()]
            ):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            return redirect_to_login(redirect_to)
    admin.site.__class__ = AdminSiteOTPRequiredMixinRedirSetup

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(LoggingGraphQLView.as_view(graphiql=True))),
    path('api/', include('banca.urls')),
    path('api/', include('demograficos.urls')),
    path('api/', include('pld.urls')),
    path('api/token-auth/', csrf_exempt(obtain_auth_token),
         name='api_token_auth'),
    path('qr/', my_image, name='qr'),
    url('^inbox/notifications/', include(notifications.urls,
                                         namespace='notifications')),
    path('', include('scotiabank.urls')),
    path("chat/", web_chat),
    path('', include('demograficos.urls')),
    path('', include('dapp.urls')),
]

if SITE in [
    "stage",
    "test",
    "prod"
]:
    urlpatterns.append(path('', include(tf_urls, "two_factor")),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
